# wlanpi-chat-bot

Chat bot for the WLAN Pi project - dev work only (this is go away soon)

*** Note that this code is still under development ***

# Installation

To install the code for dev purposes only, from the WLAN Pi CLI, execute the following commands:

```

cd /home/wlanpi

# pull the code from GitHub
sudo git clone https://github.com/WLAN-Pi/wlanpi-chat-bot.git

# change in to the new code directory
cd wlanpi-chat-bot

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
cd /home/wlanpi/wlanpi-chat-bot

# run the de-install script
./install.sh -r

# remove existing source files
cd ..
rm -rf ./wlanpi-chat-bot

```
