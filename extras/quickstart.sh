#!/usr/bin/env bash
#####################################################
#
# Quickstart script to configure chat-bot
#
#
#####################################################
if [ $EUID -ne 0 ]; then
   echo "This script must be run as root (e.g. use 'sudo')" 
   exit 1
fi

set -e

CONFIG_FILE=/etc/wlanpi-chat-bot/config.json
APP_KEY=""

get_app_key () {
    read -p "Please enter the app key of your bot : " APP_KEY
    return
}

#####################################################

main () {

    clear
    cat <<INTRO
#####################################################

            WLANPi Chat-Bot Key Setup

This script will configure the WLAN Pi chat-bot
feature with the app key to bring it online. This
allows you to send remote commands to your WLAN Pi
bot from your Telegram client.

The app key is obtained when you create your bot
on Telegram. If you have not created a bot on Telegram
yet, please exit this setup wizard and checkout the 
user guide for chat-bot:

https://github.com/WLAN-Pi/wlanpi-chat-bot/blob/main/docs/USERGUIDE.md

##################################################### 
INTRO

    read -p "Do you wish to continue? (y/n) : " yn

    if [[ ! $yn =~ [yY] ]]; then
        echo "OK, exiting."
        exit 1
    fi

    sleep 1
    # Enter app key
    clear
    cat <<KEY
#####################################################

             WLANPi Chat-Bot Key Setup

Please enter your bot app key:

##################################################### 
KEY

    get_app_key
    
    echo "Writing supplied key value..."

    # swap out app key
    sed -i "s/\"bot_token\":.*/\"bot_token\": \"$APP_KEY\",/" $CONFIG_FILE
  
    echo "App key configured."
    sleep 1

    echo "Restarting chat-bot service to activate key"
    systemctl restart wlanpi-chat-bot
    sleep 1

    clear
    cat <<COMPLETE
#####################################################

             WLANPi Chat-Bot Key Setup

 Quickstart script completed. If the script completed
 with no errors, you may now use your chat-bot (if
 the correct app key was entered).

 Please consult the chat-bot user guide for full
 details on using the bot:

 https://github.com/WLAN-Pi/wlanpi-chat-bot/blob/main/docs/USERGUIDE.md

 (Hint: send the "hi" command to your bot twice to 
 wake it up.)

##################################################### 
COMPLETE

    return
}

########################
# main
########################
main
exit 0
