import os
import re
import yaml

# TODO: automate this pull in all verbs and find 
# all combos. Identify no-noun verbs from commands
# that contain no "_" character to remove req for
# static list

# read in the verb definitions from yaml file
with open(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "verbs.yml"), "r"
) as f:

    # read in yaml file & parse in to dict
    try:
        data_dict = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        print("YAML file read error : {}".format(exc))
        exit()

supported_verbs = data_dict["supported_verbs"]
no_noun = data_dict["no_noun"]
verb_combos = data_dict["verb_combos"]


def sanitize_args(args):

    clean_args = []

    for arg in args:
        clean_arg = re.sub("[;`<>|]", "", arg)
        clean_args.append(clean_arg)

    return clean_args


def verb_expander(cmd_verb):

    for verb, abbr_list in verb_combos.items():
        if cmd_verb in abbr_list:
            return verb

    # no match, return False
    return False


def noun_combos(command_dict):

    # pull out the nouns from the global command dict
    command_list = list(command_dict.keys())
    command_list.sort()

    noun_list = []

    # build list of nouns
    for command in command_list:

        noun = ''

        # check this isn't a noun-only cmd
        if "_" in command:
            cmd_list = command.split("_")
            noun = cmd_list[1]
        else:
            noun = command

        # if unique noun, add to list
        if noun not in noun_list:
            noun_list.append(noun)
    
    # create a list of all combos for global lookup
    noun_combos = {}

    # sort the list
    noun_list.sort(reverse=True)

    for noun in noun_list:

        # put ful command in combo list
        noun_combos[noun] = noun

        # step through combos, from longest to shortest (min 2 chars)
        # if already exists, this indicate a duplicate, so flag for
        # removal
        for length in range(len(noun)-1, 1, -1):

            new_entry = noun[0:length]

            if new_entry in noun_combos.keys():
                # already exists, flag for removal
                noun_combos[new_entry] = "remove_me"
            else:
                noun_combos[new_entry] = noun

    # tidy up duplicates    

    # make a copy so we don't break iteration
    noun_combos_copy = noun_combos.copy()
    
    for noun_variant in noun_combos_copy.keys():

        if noun_combos_copy[noun_variant] == "remove_me":
            del noun_combos[noun_variant]
    
    return noun_combos

def parse_cmd(cmd_text, command_list, noun_combos):

    """
    Function to parse a string passed to this parser to find a match
    for one of the listed commands in the supported commands list

    The function also supports expansion of abbreviations of command
    verbs (e.g. "sh" expanded to "show")

    Each command is generally in the format (those in 'no-noun' list need only a verb):

    Verb noun [arg1]...[argX]

    Supported verbs include (check utils/verbs.yml for full list):

    - exec (unambiguous abbreviations: e, ex, exe)
    - set (unambiguous abbreviations: se)
    - show (unambiguous abbreviations: sh, sho)


    Parse process:

    1. Tokenize command string by whitespace
    2. Extract first token (verb)
    3. Verify if verb (or provide shortened version) is supported
    4. Expand verb if required
    5. Check if noun is required, ignore noun iteration if not
    6. Expand noun if required
    7. Iterate through command strings, adding noun until a command match is achieved
    8. Return the matched command & remaining tokens as arg list
    9. If no command match achieved, return False

    """

    # tokenize & extract noun
    tokens = cmd_text.split()
    
    # lower case to remove case sensitivity
    verb = tokens[0].lower()
    
    noun =  ''
    if len(tokens) > 1:
        # lower case to remove case sensitivity
        noun = tokens[1].lower()
    
    args = []

    # check verb for possible abbreviation expansion
    if verb not in supported_verbs:
        verb = verb_expander(verb)

    if not verb:
        return [False, []]

    cmd = verb
    arg_start = 1

    # this branch deals with a verb only command (e.g. ping)
    if verb in no_noun:

        # if noun is empty, we may have a single verb cmd (e.g. speedtest)
        if noun == "":
            if verb in no_noun:
                return [cmd, []]
        else:
            if cmd in command_list:
                # we got a match, slice off args and return the command

                for arg in list(tokens[arg_start:]):
                    args.append(arg)

                # format: [ str, list ]
                return [cmd, sanitize_args(args)]

    # this branch deals with a verb + noun command (e.g. show cdp)
    else:
        # substitute in full noun if only noun supplied
        if noun in noun_combos.keys():
            noun  =  noun_combos[noun]
        
        # Iterate through nouns to find command match by adding each token
        #for noun in nouns:

        # check if the verb needs a noun or not
        cmd = cmd + "_" + noun
        arg_start += 1

        if cmd in command_list:
            # we got a match, slice off args and return the command

            for arg in list(tokens[arg_start:]):
                args.append(arg)

            # format: [ str, list ]
            return [cmd, sanitize_args(args)]

    # no match, return False
    return [False, []]
