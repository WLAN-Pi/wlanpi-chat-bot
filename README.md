# wlanpi-telegram-bot

Telegram bot for the WLAN Pi project

*** Note that this code is still under development ***

# Installation

To install the code, from the WLAN Pi CLI, execute the following commands:

```

cd /home/wlanpi

# pull the code from GitHub
sudo git clone https://github.com/WLAN-Pi/wlanpi-telegram-bot.git

# change in to the new code directory
cd wlanpi-telegram-bot

# run the install script
./install.sh

# add in the bot key to the configuration file (update the "bot_token" field)
nano /opt/wlanpi-chat-bot/etc/config.json

# start the bot service
sudo systemctl restart wlanpi-chat-bot.service

# check the service status
sudo systemctl status wlanpi-chat-bot.service
```

To remove the code and pull in a newer version execute the following commands and then repeat the steps above

```
cd /home/wlanpi/wlanpi-telegram-bot

# run the de-install script
./install.sh -r

# remove existing source files
cd ..
rm -rf ./wlanpi-telegram-bot

```

# Commands

The following commands are available from the Telegram bot to gather info from the WLAN Pi or initiate actions:

```
Available commands:

exec iperf
exec iperf3
exec ping
exec reboot
exec speedtest
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
show ver
(Type 'info' for startup status msg)
```

To see the list of commands available, type `help` or `?` when sending messages to the WLANP Pi.

# Notes

1. Without a bot key configured, the service will not currently start.
2. The start-up message from the WLAN Pi is not seen the first time that the bot service is run (as the chat ID has not yet been derived). This is a one-time issue.
3. Logging levels are "info" by default and logging is sent to syslog



