import os
import re

import yaml

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


def parse_cmd(cmd_text, command_list):

    """
    Function to parse a string passed to this parser to find a match
    for one of the listed commands in the supported commands list

    The function also supports expansion of abbreviations of command
    verbs (e.g. "sh" expanded to "show")

    Each command is generally in the format (those in 'no-noun' list need only a verb):

    Verb noun [arg1]...[argX]

    Supported verbs include (check utils/verbs.yml for gull list):

    - exec (unambiguous abbreviations: e, ex, exe)
    - set (unambiguous abbreviations: se)
    - show (unambiguous abbreviations: sh, sho)


    Parse process:

    1. Tokenize command string by whitespace
    2. Extract first token (verb)
    3. Verify if verb (or provide shortened version) is supported
    4. Expand verb if required
    5. Check if noun is required, ignore noun iteration if not
    5. Iterate through command string, adding nouns until a command match is achieved
    6. Return the matched command & remaining tokens as arg list
    7. If no command match achieved, return False

    """

    # tokenize & extract noun
    tokens = cmd_text.split()
    verb = tokens[0]
    nouns = tokens[1:]
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

        # if nouns list is zero, we may have a single verb cmd (e.g. speedtest)
        if len(nouns) == 0:
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
        # Iterate through nouns to find command match by adding each token
        for noun in nouns:

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
