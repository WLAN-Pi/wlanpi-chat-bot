import re


class Parser:

    """
    Class for command parsing
    """

    def __init__(self, global_cmd_dict):

        self.supported_verbs = []
        self.supported_nouns = []
        self.no_noun = []  # cmds that are verb only (e.g.ping)
        self.verb_combos_dict = {}
        self.noun_combos_dict = {}

        self.command_list = list(global_cmd_dict.keys())
        self.command_list.sort()

        # populate verb & noun lists for parsing
        self.verb_combos(global_cmd_dict)
        self.noun_combos(global_cmd_dict)

    def sanitize_args(self, args):
        """
        clean up any dodgy chars to stop bad
        people injecting chars to do things
        we'd prefer they don't do
        """
        clean_args = []

        for arg in args:
            clean_arg = re.sub("[;`<>|]", "", arg)
            clean_args.append(clean_arg)

        return clean_args

    def verb_expander(self, cmd_verb):
        """
        Expand a possible verb abbrevation if found in combo list

        Args:
            cmd_verb (string): possible verb

        Returns:
            string or False: expanded verb or False if not found
        """

        for verb, abbr_list in self.verb_combos_dict.items():
            if cmd_verb in abbr_list:
                return verb

        # no match, return False
        return False

    def noun_expander(self, cmd_noun):
        """
        Expand a possible noun abbrevation if found in combo list

        Args:
            cmd_noun (string): possible noun

        Returns:
            string or False: expanded noun or False if not found
        """

        for noun, abbr_list in self.noun_combos_dict.items():
            if cmd_noun in abbr_list:
                return noun

        # no match, return False
        return False

    def combo_engine(self, word_list):
        """
        Take the supplied word ist and create all possible
        unique combinations down to 2 chars

        Args:
            word_list (list): list of words to be processed

        Returns:
            word_combos (dict): dict of all possible combinations
                in format "abbr": "full word"
        """

        word_combos = {}

        # sort the list
        word_list.sort(reverse=True)

        for word in word_list:

            # put ful command in combo list
            word_combos[word] = word

            # step through combos, from longest to shortest (min 2 chars)
            # if already exists, this indicate a duplicate, so flag for
            # removal
            for length in range(len(word) - 1, 1, -1):

                new_entry = word[0:length]

                if new_entry in word_combos.keys():
                    # already exists, flag for removal
                    word_combos[new_entry] = "remove_me"
                else:
                    word_combos[new_entry] = word

        # tidy up duplicates
        # make a copy so we don't break iteration
        word_combos_copy = word_combos.copy()

        for word_variant in word_combos_copy.keys():

            if word_combos_copy[word_variant] == "remove_me":
                del word_combos[word_variant]

        return word_combos

    def verb_combos(self, command_dict):
        """
        Figure out all possible verb combinations so that a
        noun can be types with a minimum unique combination
        of characters (e.g. type "sh" instead of show)

        Args:
            command_dict (dict): dictionary of all commands (noun + verb)

        Returns:
            [dict]: every possible verb abbreviation combination that uniquely
                    idenitifes a verb, e.g.
                    {
                        "pu":       "publicip",
                        "pub":      "publicip",
                        "publi":    "publicip",
                        "public":   "publicip",
                        "publici":  "publicip",
                        "publicip": "publicip"
                    }
        """
        verb_list = []

        # build list of verbs
        for command in self.command_list:

            verb = ""

            # check this isn't a noun-only cmd
            if "_" in command:
                cmd_list = command.split("_")
                verb = cmd_list[0]
            else:
                self.no_noun.append(command)
                verb = command

            # if unique verb, add to list
            if verb not in verb_list:
                verb_list.append(verb)
                self.supported_verbs.append(verb)

        self.verb_combos_dict = self.combo_engine(self.supported_verbs)

    def noun_combos(self, command_dict):
        """
        Figure out all possible noun combinations so that a
        noun can be types with a minimum unique combination
        of characters (e.g. type "sh" instead of show)

        Args:
            command_dict (dict): dictionary of all commands (noun + verb)

        Returns:
            [dict]: every possible noun abbreviation combination that uniquley
                    idenitifes a noun, e.g.
                    {
                        "sh":   "show",
                        "sho":  "show",
                        "show": "show"
                    }
        """
        # build list of nouns
        for command in self.command_list:

            noun = ""

            # check this isn't a verb-only cmd
            if "_" in command:
                cmd_list = command.split("_")
                noun = cmd_list[1]
            else:
                continue

            # if unique noun, add to list
            if noun not in self.supported_nouns:
                self.supported_nouns.append(noun)

        self.noun_combos_dict = self.combo_engine(self.supported_nouns)

    def parse_cmd(self, cmd_text):

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

        # tokenize & extract verb
        tokens = cmd_text.split()

        # lower case to remove case sensitivity
        verb = tokens[0].lower()

        noun = ""
        if len(tokens) > 1:

            if verb in self.no_noun:
                # no noun will accompany the verb,
                # everything else if args
                noun = False
            else:
                noun = tokens[1].lower()
                # lower case to remove case sensitivity
                if noun not in self.supported_nouns:
                    # assume this is an abbreviation to expand
                    noun = self.noun_expander(noun)

        args = []

        # check verb for possible abbreviation expansion
        if verb not in self.supported_verbs:
            verb = self.verb_expander(verb)

        if not verb:
            return [False, []]

        cmd = ""
        arg_start = 1

        if verb in self.no_noun:
            # verb-only cmd
            cmd = verb
        else:
            # verb + noun cmd
            arg_start = 2
            cmd = f"{verb}_{noun}"

        if cmd in self.command_list:
            # we got a match, slice off args and return the command

            for arg in list(tokens[arg_start:]):
                args.append(arg)

            # format: [ str, list ]
            return [cmd, self.sanitize_args(args)]
        else:
            # no match, return False
            return [False, []]
