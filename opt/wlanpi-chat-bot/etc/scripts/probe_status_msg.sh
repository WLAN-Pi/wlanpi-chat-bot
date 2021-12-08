#!/usr/bin/env bash

#Author: Jiri Brejcha, jirka@jiribrejcha.net
#Sends current WLAN Pi IP address and other useful details to you in a Telegram message. Requires internet connection.

#Collect all data
ETH0SPEED=$(ethtool eth0 2>/dev/null | grep -q "Link detected: yes" && ethtool eth0 2>/dev/null | grep "Speed" | sed 's/....$//' | cut -d ' ' -f2  || echo "disconnected")
ETH0DUPLEX=$(ethtool eth0 2>/dev/null | grep -q "Link detected: yes" && ethtool eth0 2>/dev/null | grep "Duplex" | cut -d ' ' -f 2 || echo "disconnected")
HOSTNAME=$(hostname)
UPTIME=$(uptime -p | cut -c4-)
MODE=$(cat /etc/wlanpi-state)
ETH0IP=$(ip a | grep "eth0" | grep "inet" | grep -v "secondary" | head -n1 | cut -d '/' -f1 | cut -d ' ' -f6)
UPLINK=$(ip route show | grep "default via" | cut -d " " -f5)
UPLINKIP=$(ip a | grep "$UPLINK" | grep "inet" | grep -v "secondary" | head -n1 | cut -d '/' -f1 | cut -d ' ' -f6)
NEIGHBOUR=$(grep -q "Name:" /tmp/lldpneigh.txt 2>/dev/null && cat /tmp/lldpneigh.txt | sed 's/^Name:/Connected to:/g' | sed 's/^Desc:/Port description:/g' | sed 's/^IP:/Neighbour IP:/g' | sed -z 's/\n/%0A/g')
if [ -z "$NEIGHBOUR" ]; then
  NEIGHBOUR=$(grep -q "Name:" /tmp/cdpneigh.txt 2>/dev/null && cat /tmp/cdpneigh.txt | sed 's/^Name:/Connected to:/g' | sed 's/^Port:/Port description:/g' | sed 's/^IP:/Neighbour IP:/g' |sed 's/^SW:/Software version:/g' | sed -z 's/\n/%0A/g')
fi

#Get public IP data
DATAINJSON=$(timeout 3 curl -s 'ifconfig.co/json')
PUBLICIP=$(echo "$DATAINJSON" | jq -r '.ip')
PUBLICIPCOUNTRY=$(echo "$DATAINJSON" | jq -r '.country')
PUBLICIPASNORG=$(echo "$DATAINJSON" | jq -r '.asn_org')
PUBLICIPHOSTNAME=$(echo "$DATAINJSON" | jq -r '.hostname')
PUBLICIPASN=$(echo "$DATAINJSON" | jq -r '.asn')

if [ -z "$ETH0IP" ]; then
  CURRENTIP="$UPLINKIP"
else
  CURRENTIP="$ETH0IP"
fi

#Compose the message
TEXT=""
TEXT+="%f0%9f%9f%a2 <b>$HOSTNAME is now online</b> %0A"
if [ "$ETH0IP" ]; then
  TEXT+="Eth0 IP address: <code>$ETH0IP</code> %0A"
fi
if [[ "$ETH0SPEED" == "disconnected" ]]; then
  TEXT+="Eth0 is down %0A"
else
  TEXT+="Eth0 speed: $ETH0SPEED %0A"
  TEXT+="Eth0 duplex: $ETH0DUPLEX %0A"
fi
TEXT+="WLAN Pi mode: $MODE %0A"
TEXT+="Uptime: $UPTIME %0A"

if [ ! -z "$NEIGHBOUR" ]; then
  TEXT+="%0A"
  TEXT+="$NEIGHBOUR"
fi

TEXT+="%0A"
TEXT+="Uplink to internet: $UPLINK %0A"
if [[ "$UPLINK" != "eth0" ]]; then
  TEXT+="Local $UPLINK IP address: $UPLINKIP %0A"
fi
TEXT+="Public IP: <code>$PUBLICIP</code>, <code>$PUBLICIPHOSTNAME</code> %0A"

if [ ! -z "$CURRENTIP" ]; then
  TEXT+="%0A"
  TEXT+="Web interface: http://$CURRENTIP %0A"
  #TEXT+="Web console: https://$CURRENTIP:9090 %0A"
  TEXT+="SSH: <code>ssh://wlanpi@$CURRENTIP</code> %0A"
  #TEXT+="Copy file to TFTP server: copy flash:filename tftp://$CURRENTIP %0A"
fi

echo $TEXT