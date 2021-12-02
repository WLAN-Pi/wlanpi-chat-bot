# Adding YAML Commands

Commands may be added to the chatbot using a call to an existing external script.

They must be a simple call that returns a block of text that can be displayed in the chat bot window.

To add a command, simply create a yml file to the `wlanpi-commands/yaml` directory, formatted as shown below.

# Example

```
---
 command: show_lldp
 exec: cat /tmp/lldpneigh.txt 2> /dev/null || echo \"No LLDP file found\"
 progress_msg: Getting LLDP neighbours
 emoji: page
 help_short: Show probe LLDP neighbours
 help_long: "show cdp: Show the LLDP neighbours of the probe. \n\n
             (Note that neigbours may take up to 60 seconds to be reported after a boot \n)"  
```

All files must contain the following fields:
 - command: this is the name of the command, with the verb and noun separated by an underscore (the underscore is removed during rendering, but is mandatory). Note that if new verbs or verbs that required no noun are created, the must be added to 'utils/verbs.yml'. Acceptable abbreviations for each verb must also be added to the same file.
 - exec: either a series of commands or a script to be called
 - progress_msg: a message to be displayed during while the user is waiting for the command to complete
 - emoji: name of an emoji in emojis.py (can be empty value if none required)
 - help_short: string to be shown in compact display mode
 - help_long: string to be shown in full display mode