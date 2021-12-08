[![packagecloud-badge](https://img.shields.io/badge/deb-packagecloud.io-844fec.svg)](https://packagecloud.io/)

# wlanpi-chat-bot

A telegram chat bot for the WLAN Pi.

*** WARNING: this project is currently unstable and under development ***

## Commands

The following commands are available from the chat bot to gather info from the WLAN Pi or initiate actions:

```
Available commands:

iperf
iperf3
ping
reboot
set display mode
set display width
show cdp
show lldp
show mode
show publicip
show reachability
show status
show summary
show time
show uptime
show ver
speedtest

(Type 'info' for startup status msg)
```

To see the list of commands available, type `help` or `?` when sending messages to the WLANP Pi.

![Screenshot](chatbot/images/screenshot.png)

## Debian Packaging

If you'd like to build the Debian package yourself, review the following instructions.

Install build depends:

```bash
sudo apt-get install build-essential debhelper devscripts equivs python3-pip python3-all python3-dev python3-setuptools dh-virtualenv
```

Install Python depends so that the tooling doesn't fail when it tries to evaluate which tests to run.

```bash
python3 -m pip install mock
```

Clone and install the package:

```bash
# Build the deb package
git clone https://github.com/WLAN-Pi/wlanpi-chat-bot.git
cd wlanpi-telegram-bot
sudo dpkg-buildpackage -us -uc

# The deb package is here
cd ..

# Install the package
sudo apt install ./wlanpi-chat-bot_1.0.0_armhf.deb 

# Configure your Telegram API key
sudo nano /opt/wlanpi-chat-bot/etc/config.json

# Restart twice so that Chat ID is obtained and you receive a new status message from the bot
sudo systemctl restart wlanpi-chat-bot; sleep 5; sudo systemctl restart wlanpi-chat-bot 

# Uninstall the package while keeping the Chat Bot config file with your API key
sudo apt remove wlanpi-chat-bot

# Remove the package completely including Chat Bot config file with your API key
sudo apt purge wlanpi-chat-bot
```

## Configure Chat-Bot

1. Create a new Telegram account if you do not have one already. Start the Telegram app.
2. Let’s create a new Telegram bot. Find a person called Botfather and send them a message saying /newbot.
3. Follow the instructions to create a new bot.
4. After the new bot is created, copy the API key to a text editor.
5. Edit the file `/opt/wlanpi-chat-bot/etc/config.json` and enter your API key in to the the `"bot_token"` field:

```
{
    "telegram": {
        "bot_token": "1233735614:AAHe9eHOP_uCe6773bWjQTNvHT_llYHmFSw",
        "chat_id": "",
        "display_mode": "full",
        "display_width": "30",
        "yaml_cmds": "/opt/wlanpi-chat-bot/etc/commands"
    }
}
```

6. Restart the chat service to read the updated configuration file:

```bash
systemctl restart wlanpi-chat-bot
```

7. In Telegram, send a message to the newly created bot (e.g. show status), this will provide the bot with the chat_id it needs to start communicating. You may have to do this a couple of times to kick it into life. Once the bit is responding, you're good go. You don't need to do this again, it's a one-time operation.

8. Send the bot a "?" to see the commands available to you. Have fun :)
