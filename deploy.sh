#!/bin/bash
echo "🚀 PUBLIC DorkBot DEPLOY"

# Clone & setup
git clone https://github.com/your-repo/dorkbot-public /root/dorkbot || mkdir -p /root/dorkbot
cd /root/dorkbot

# Install
pip3 install -r requirements.txt

# Copy files
cp pyrogram_bot.py /root/
cp proxies.txt /root/

# Auto setup
echo "🔧 AUTO SETUP - Enter your details:"
python3 setup.py

# Proxies
curl -s "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http" > /root/proxies.txt

echo "🎉 DEPLOYED! Run: python3 /root/pyrogram_bot.py"
echo "Or: screen -S dorkbot python3 /root/pyrogram_bot.py"
