

supported_verbs = [ 'show', 'exec', 'set', 'run']

def verb_expander(cmd_verb):

    verb_combos = {
        "show": ['sh', 'sho'],
        "set": ['se'],
        "exec": ["e", "ex", "exe"],
        "run": ["r", "ru"]
    }

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

    Each command is in the format:

    Verb noun1 [noun2]...[nounX] [arg1]...[argX]

    Supported verbs:

    - show (unambiguous abbreviations: sh, sho)
    - set (unambiguous abbreviations: se)
    - exec (unambiguous abbreviations: e, ex, exe)
    - run (unambiguous abbreviations: r, ru)

    Parse process:

    1. Tokenize command string by whitespace
    2. Extract first token (verb)
    3. Verify if verb (or provide shortened version) is supported
    4. Expand verb if required
    5. Iterate through command string, adding nouns until a command match is achieved
    6. Return the matched command & remaining tokens as arg list
    7. If no command match achieved, return False

    """

    # tokenize & extract noun
    tokens = cmd_text.split()
    verb = tokens[0]
    args = []

    # check verb for possible abbreviation expansion
    if verb not in supported_verbs:
        verb = verb_expander(verb)
    
    if not verb:
        return [ False, [] ]
    
    # Iterate through nouns to find command match by adding each token
    nouns =  tokens[1:]
    cmd = verb

    arg_start = 1
    for noun in nouns:
        cmd = cmd + "_" + noun
        arg_start += 1

        if cmd in command_list:
            # we got a match, slice off args and return the command

            for arg in list(tokens[arg_start:]):
                args.append(arg)

            # format: [ str, list ]
            return [cmd, args]
    
    # no match, return False
    return [ False, [] ]
    



    
