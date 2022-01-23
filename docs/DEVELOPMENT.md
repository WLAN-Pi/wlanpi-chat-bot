# Development Setup Instructions

## Initial Setup

The following steps are the initial instructions to clone the codebase locally and setup a virtualenv.

1. Clone repo:

```
git clone https://github.com/WLAN-Pi/wlanpi-chat-bot.git && cd wlanpi-chat-bot
```

2. Create virtualenv:

```
python3 -m venv venv
```

3. Activate venv:

```
source venv/bin/activate
```

5. Update pip, setuptool, and wheel (this is only done once)

```
pip install -U pip setuptools wheel
```

6. Install requirements

```
pip install -r requirements.txt
```

## Executing the wlanpi-chat-bot module

Ok, now should be read to run the code. This version of the chat-bot is packaged into a module. So, we need to instruction Python to run it as a module with the `-m` option.

1. If developing on a WLAN Pi that is already running wlanpi-chat-bot, stop the servie before running up our development instance

```
sudo systemctl stop wlanpi-chat-bot
# check it stopped
sudo systemctl status wlanpi-chat-bot

```

2. We need to run chat-bot as sudo, which means we'll need to pass along the location of the Python environment to sudo like this:

```
sudo venv/bin/python3 -m chatbot
```

If you'd like to run chat-bot in debug mode for testing, run with the "--debug" option:

```
sudo venv/bin/python3 -m chatbot --debug
```

If you'd like to pass your chat-bot app token for testing, pass it in via the "--bot_token" option:

```
sudo venv/bin/python3 -m chatbot --bot_token
```

Further reading on executing modules with Python at <https://docs.python.org/3/library/runpy.html>.

## Cheatsheet

New environment?

```
cd ~/wlanpi-chat-bot
python3 -m venv venv
source venv/bin/activate
pip install -U pip setuptools wheel
pip install -r requirements.txt
sudo systemctl stop wlanpi-chat-bot
sudo systemctl status wlanpi-chat-bot --no-pager
sudo venv/bin/python3 -m chatbot
```

Is your development environment already setup?

```
cd ~/wlanpi-chat-bot
source venv/bin/activate
sudo systemctl stop wlanpi-chat-bot
sudo systemctl status wlanpi-chat-bot --no-pager
sudo venv/bin/python3 -m chatbot
```