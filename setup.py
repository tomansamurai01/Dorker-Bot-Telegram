#!/usr/bin/env python3
"""
AUTO SETUP - Gets token/API from user input → Creates config
"""

import os, asyncio, json
from pyrogram import Client
from pyrogram.raw.functions.messages import GetDialogs
from pyrogram.raw.types import InputPeerEmpty

print("🚀 **DorkBot v4 PUBLIC AUTO SETUP**")
print("=" * 50)

# 1. BOT TOKEN (Public input)
BOT_TOKEN = input("📱 BotFather Token (123456:ABC...): ").strip()
if not BOT_TOKEN.startswith(('1', '2')) or ':' not in BOT_TOKEN:
    print("❌ Invalid token!")
    exit(1)

# 2. API_ID + API_HASH (Auto guide)
API_ID = input("🔑 API_ID (my.telegram.org): ").strip()
API_HASH = input("🔑 API_HASH (my.telegram.org): ").strip()

if not API_ID.isdigit() or len(API_HASH) < 20:
    print("❌ Get from: my.telegram.org → API development tools")
    exit(1)

# 3. Test connection
print("🔄 Testing connection...")
try:
    async def test():
        app = Client("test", api_id=int(API_ID), api_hash=API_HASH, bot_token=BOT_TOKEN)
        await app.start()
        me = await app.get_me()
        print(f"✅ Bot ready: @{me.username}")
        await app.stop()
    
    asyncio.run(test())
except:
    print("❌ Connection failed!")
    exit(1)

# 4. CREATE AUTO CONFIG
config = {
    "API_ID": API_ID,
    "API_HASH": API_HASH,
    "BOT_TOKEN": BOT_TOKEN,
}

with open("/root/config.json", "w") as f:
    json.dump(config, f, indent=2)

print("\n🎉 **AUTO SETUP COMPLETE!**")
print("📁 Created: /root/config.json")
print("🚀 Run: python3 /root/pyrogram_bot.py")
