#!/bin/bash
pip3 install -r requirements.txt
mkdir -p /root/{telegram_files,tools}
cp pyrogram_bot.py /root/
cp proxies.txt /root/
chmod +x /root/pyrogram_bot.py
echo "✅ Pyrogram setup!"
echo "1. my.telegram.org → Get API_ID + API_HASH"
echo "2. Edit /root/.env"
echo "3. python3 /root/pyrogram_bot.py"
