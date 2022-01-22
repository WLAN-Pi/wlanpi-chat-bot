# User Guide for WLAN Pi Chat-Bot

## Overview
The WLAN Pi chat-bot is a Telegram bot that allows a number of remote operations to be performed on a WLAN Pi that has Internet connectivity. These include operations such as checking the status of the WLAN Pi and running tests such as speedtest.

(__Note: see [Security Considerations](#security-considerations) below before using chat-bot__)

There are three steps to configure the chat-bot:

 - Install the Telegram application on a mobile device and create a Telegram account 
 - Configure yourself a bot on Telegram (this will be your WLAN Pi bot)
 - Configure an API key on the WLAN Pi to allow it to talk to your Telegram bot

These steps are detailed in the [Set-up section](#set-up) below.

Once the bot is operational, there are a number of commands that can be executed to obtain information and execute various tests and operations directly on the WLAN Pi. This provides a useful remote interface to the WLAN Pi. Operating the bot command interface covered in the [Using Chat-bot section](#using-chat-bot) below. 

## Set-up
The 3 steps required to set-up chat-bot are detailed below:

### Create a Telegram Account

Creating a Telegram account is an easy process. You need to download the Telegram app to your Apple or Android phone and then use the account creation options within the app. Here is an article about the process, but it should be pretty easy to follow the steps provided in the app:

 - [How to make a Telegram account ](https://www.businessinsider.com/how-to-make-a-telegram-account)

 (Note: you will need a phone number to complete the free sign-up for Telegram)

### Telegram

Once you have your Telegram account, you'll need to create a Telegram bot to talk with the WLAN Pi. This is a one-time operation. Once completed, you will be able to access the WAN Pi via this bot each time your WLAN Pi connects to the Interet.

Here are the basic instructions of how to configure the bot:

1. Start the Telegram app
2. Create a new Telegram bot: find a person called Botfather and send them a message saying `/newbot` (__Note: see [Security Considerations](#security-considerations) below!__)
3. Follow the on-screen instructions to create a new bot and make a note of the API key that is provided
4. After the new bot is created, copy the API key to a text editor for later use

### Chat-bot

To configure the WLAN Pi to talk with the Telegram chat-bot, we need to configure the WLAN Pi with the API key provided when the bot was set up. There are three methods available:

1. Run the "quickstart" script to initiate a CLI_based wizard to configure the app key quickly & easily. you will need to be able to SSH to the WAN Pi to execute this script. Once you have SSH access, execute the following CLI command:

```
sudo quickstart-chat-bot
```

Follow the on-screen instructions t configire your app key and restart chat-bot.

2. SSH to the WLAN pi and edit the file `/etc/wlanpi-chat-bot/config.json`. Enter your API key in to the the `"bot_token"` field:

```
wlanpi@wlanpi:~$ sudo nano /etc/wlanpi-chat-bot/config.json`
```

```
{
    "telegram": {
        "bot_token": "1233735614:AAHe9eHOP_uCe6773bWjQTNvHT_llYHmFSw",
        "chat_id": "",
        "username": "",
        "display_mode": "full",
        "display_width": "30",
    }
}
```
To ensure the API key is read correctly, restart the chat-bot process on the WLAN Pi:

```
wlanpi@wlanpi:~$ sudo systemctl restart wlanpi-chat-bot
```

3. For a completely headless configuration, it's possible to add a file to the micro-SD card that runs the WLAN Pi image. Pop the SD card out of the WLAN Pi and using a SD card-to-USB adapter, access the SD card via a USB port on your laptop or MAC. There is a readable partition called "boot" on the SD card where the chat-bot API key may be placed. 

Create a file called `wlanpi_bot.key` in the `boot` partition. Create the file with a plain text editor and add a single line that contains just the API key that was provided during bot creation. Here are a couple of screen-shots that show the file created on a Windows machine and a Mac:

![Screenshot](images/boot_partition_windows.png)

![Screenshot](images/boot_partition_mac.png)

Once the WLAN Pi boots up and reads the file from the boot partition, the API key is added to the WLAN Pi bot config file and removed from the boot partition for security purposes.

3. Once the API key is in-place via one of the two methods outlined above, its time to wake up the bot and make sure you can send it messages.

With the WLAN Pi connected to the Internet, open up your Telegram client and send a message to the bot. You can try : `hi`. You will likely get no response to your first message. Don't worry...send a second message: `hi`. You should now receive a response. Your bot is now keyed to you user ID  and username and will respond only to you. You will not need to repeat this wake-up process - each time you switch on the WLAN Pi and it is connected to the Internet, it will establish comms with your Telegram client.

## Using Chat-Bot

To interact with the WLAN Pi chat-bot, commands are entered in to the Telegram app command UI. To see which commands are available, simply enter a "?" and hit enter. This will show all commands available from the WLAN Pi:

![Screenshot](images/chatbot-show-commands.png)

### Entering Commands

Most commands are made up of a two parts:

    <verb> <noun>

For instance, to see CDP neighbors of a WLAN Pi, the command `show cdp` is used. In this instance, `show` is the verb and it is followed by the noun `cdp`.

```
show cdp
```

Note that a small number of commands are single-word (verb-only) commands. For instance, `speedtest` are verb-only. Here is screen-shot showing the `speedtest` command:

![Screenshot](images/chatbot-speedtest.png)

### Command Abbreviations

Typing the full command each time to perform an operation can be laborious. Therefore, it is possible to enter the minimum unique representation of each command. For instance, instead of entering the full command `speedtest`, this could be abbreviated to "speed", "spee", "spe" or "sp". "A single `s` would not be valid as this would clash with the `show` commands.

Note that both the verb and noun can be abbreviated, so that `show summary` command can be entered as `sh sum`:

![Screenshot](images/chatbot-sh-sum.png)

### On-screen Help 

To gain additional help while using the chat bot, there are a couple of additional methods of finding useful information.

To get an extended description of how to use chat-bot the command `help` may be used:

![Screenshot](images/chatbot-help.png)

If help is required for a particular command, it may be prefixed with the word `help` to gain addition insights such as command syntax. For example, to get help about the `show publicip` command, `help sh pub` may be used:

![Screenshot](images/chatbot-help-sh-pub.png)

# Security Considerations
Although comms to and from the WLAN Pi chat-bot is limited to just your Telegram user account, it is worth noting that all bot names are publicly searchable on Telegram. This means that people are able to search for your bot from their Telegram client. If they find the bot, they are not able to execute commands, but who knows what types of clever exploits may surface in the future?

For this reason, it is definitely worth naming your Telegram bot with a non-obvious name (e.g. do not include the phrase "wlanpi" in your bot name).

As the public nature of telegram bots is a concern, a number of techniques have been employed or are suggested to provide several layers of protection. Again, Telegram bots are, by the nature of their current implementation on the Telegram platform, publicly available. To restrict access, the following techniques are suggested, or have been implemented by the WLAN Pi team:

1. The chat-bot module is available as an optional module that you may install on to the WLAN Pi. Ensure you understand the risks before installing the chat-bot
2. When creating your bot on Telegram, use a name that is not obviously a WLAN Pi. Use something that is meaningful to you and is not easily guessable for someone trying to find your bot on the public search tool provided by Telegram. (NOTE: the bot  name is not the hostname of your WLAN Pi, it is the bot name assigned when creating the bot account on Telegram)
3. When the WLAN Pi bot is initialized with the required app key, it will use only the user-id and user account name that initially sends it a message (i.e. you) for subsequent comms. If messages are received from other user accounts and/or other user-id's, messages are dropped without processing. This ensures that only messages sent by you are processed by the WLAN Pi bot.
4. To limit any user-supplied input from trying to execute unintended commands on the WLAN Pi itself (e.g. by supplying additional characters to command arguments to trigger other OS-level commands), no commands are provided that required arguments to be supplied. Only commands that match a list of known commands are accepted, with no additional arguments accepted or processed.   



