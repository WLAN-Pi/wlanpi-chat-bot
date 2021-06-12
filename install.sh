#!/bin/bash

BASEDIR=/opt/wlanpi-chat-bot

if [ "$1" == '-r' ]; then
    echo "Removing WLAN Pi Chat bot..."
    sudo systemctl stop wlanpi-chat-bot.service
    sudo systemctl disable wlanpi-chat-bot.service
    sudo rm /lib/systemd/system/wlanpi-chat-bot.service
    sudo systemctl reset-failed
    sudo rm -rf $BASEDIR
    echo "Removed."
else
    echo "Installing WLAN Pi Chat bot..."
    sudo mkdir -p $BASEDIR
    sudo cp wlanpi-chat-bot $BASEDIR
    sudo cp version.txt $BASEDIR

    sudo cp -R ./transports $BASEDIR
    sudo cp -R ./utils $BASEDIR
    sudo cp -R ./etc $BASEDIR
    sudo cp -R ./wlanpi_commands $BASEDIR
    sudo cp -R ./scripts $BASEDIR

    sudo chmod +x $BASEDIR/wlanpi-chat-bot
    sudo chmod +x $BASEDIR/scripts/probe_status_msg.sh

    echo "Installling required python modules (please wait)..."
    sudo python3 -m pip install -r requirements.txt

    cd ./scripts
    sudo install -p -m 644 wlanpi-chat-bot.service /lib/systemd/system/wlanpi-chat-bot.service
    sudo systemctl enable wlanpi-chat-bot.service
    sudo systemctl start wlanpi-chat-bot.service
    echo "Bot service status:"
    echo ""
    echo "=============================================================="
    sudo systemctl status wlanpi-chat-bot.service
    echo "=============================================================="
fi

# sudo systemctl disable wlanpi-chat-bot.service
# sudo rm /lib/systemd/system/wlanpi-chat-bot.service
# sudo systemctl reset-failed
# sudo systemctl status wlanpi-chat-bot.service
