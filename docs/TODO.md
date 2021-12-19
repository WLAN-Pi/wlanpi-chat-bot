# TODO

Roadmap items for the wlanpi-chat-bot module.

# Short-term

 - Lower-case first letter of verb to cater for auto captitalization on phone apps
 - Create user guide

# Medium-term
- Add features from FPMS to Chat-bot. Candidates for move to wlanpi-core API:
    - show_interfaces (wlanpi-fpms: modules/network.py)
    - show_wlan_interfaces (wlanpi-fpms: modules/network.py)
    - show_eth0_ipconfig (wlanpi-fpms: modules/network.py)
    - show_vlan (wlanpi-fpms: modules/network.py)
    - show_lldp_neighbour (wlanpi-fpms: modules/network.py)
    - show_cdp_neighbour (wlanpi-fpms: modules/network.py)
    - show_publicip  (wlanpi-fpms: modules/network.py)
    - show_reachability (wlanpi-fpms: modules/utils.py)
    - show_reachability (wlanpi-fpms: modules/utils.py)
    - show_speedtest (wlanpi-fpms: modules/utils.py)
    - show_wpa_passphrase (wlanpi-fpms: modules/utils.py)
    - show_ufw (wlanpi-fpms: modules/utils.py)
- Move bash-script based utils to API calls in wlanpi-core:
    - set/show hostname (wlanpi-common: wlanpi-hostname.sh)
    - set/show regdomain (wlanpi-common: wlanpi-reg-domain.sh)
    - set/show timezone (wlanpi-common: wlanpi-timezone.sh)
- Move chat-bot utils to wlanpi-core (for use by web UI & FPMS too?)
    - get_uptime (wlanpi-chat-bot: utils/uptime.py)
# Long-term

TBA