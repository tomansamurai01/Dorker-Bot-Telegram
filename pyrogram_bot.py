#!/usr/bin/env python3
"""
DorkBot v4 PUBLIC - Auto config from /root/config.json
"""

import os, json, asyncio, random
import logging
from pathlib import Path
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import cloudscraper
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)

# 🔥 AUTO LOAD CONFIG (Public)
try:
    with open("/root/config.json") as f:
        config = json.load(f)
    API_ID = int(config["API_ID"])
    API_HASH = config["API_HASH"]
    BOT_TOKEN = config["BOT_TOKEN"]
    print("✅ Config loaded!")
except:
    print("❌ Run: python3 auto_setup.py first!")
    exit(1)

class PublicDorkBot:
    def __init__(self):
        self.proxies_file = "/root/proxies.txt"
        Path("/root/telegram_files").mkdir(exist_ok=True)
        self.proxies = self.load_proxies()
        self.ua = UserAgent()
        self.scraper = cloudscraper.create_scraper()
    
    def load_proxies(self):
        try:
            with open(self.proxies_file) as f:
                return [l.strip() for l in f if ':' in l.strip()]
        except:
            return []

bot = PublicDorkBot()
app = Client("dorkbot_public", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# DORKS (Same fast)
DORKS = {
    "$1": ['inurl:(donate|checkout) "1.00|$1"', '"1.00" braintree', 'intext:"$1" trial'],
    "$5": ['inurl:checkout "5.00|$5"', '"$5" premium'],
    "$10": ['inurl:donate "10.00|$10"', '"$10" product']
}

@app.on_message(filters.command("start"))
async def start(client, message):
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("💰 $1 Sites", callback_data="scan_1")],
        [InlineKeyboardButton("💵 $5 Sites", callback_data="scan_5")],
        [InlineKeyboardButton("💎 $10 Sites", callback_data="scan_10")],
        [InlineKeyboardButton("📁 Files", callback_data="files")]
    ])
    await message.reply_text(
        "🔥 **PUBLIC DorkBot v4**\n\n"
        "⚡ Pyrogram • Live hits • Auto-setup", 
        reply_markup=kb, parse_mode="Markdown"
    )

@app.on_callback_query(filters.regex(r"^scan_"))
async def fast_scan(client, query):
    amount = {"1": "$1", "5": "$5", "10": "$10"}[query.data.split("_")[1]]
    await query.answer(f"⚡ {amount} scan...")
    
    hits = await bot.fast_dork(amount)
    if hits:
        await bot.send_hits(query.message.chat.id, amount, hits)
    else:
        await query.message.reply("❌ No hits")

async def fast_dork(self, amount):
    """⚡ ULTRA FAST"""
    hits = []
    for dork in DORKS[amount]:
        try:
            proxy = random.choice(self.proxies) if self.proxies else None
            url = f"https://www.google.com/search?q={dork.replace(' ', '+')}&num=30"
            resp = self.scraper.get(url, proxy=proxy, timeout=5)
            
            soup = BeautifulSoup(resp.text, 'html.parser')
            for a in soup.find_all('a', href=True):
                href = a['href']
                if href.startswith('http') and 'google' not in href:
                    hits.append(href.split('&')[0])
            
            await asyncio.sleep(0.3)
        except:
            continue
    return list(set(hits))[:100]

PublicDorkBot.fast_dork = fast_dork

async def send_hits(self, chat_id, amount, hits):
    """📤 Instant file send"""
    timestamp = datetime.now().strftime("%H%M%S")
    file_path = f"/root/telegram_files/public_hits_{amount}_{timestamp}.txt"
    
    with open(file_path, "w") as f:
        f.write(f"PUBLIC {amount} HITS - {len(hits)}\n" + "="*40 + "\n\n")
        for i, hit in enumerate(hits, 1):
            f.write(f"{i}. {hit}\n")
    
    await app.send_document(
        chat_id, file_path,
        caption=f"🎯 **PUBLIC {amount}** ({len(hits)} hits)\n🔥 Live Google",
        filename=f"public_{amount}_hits.txt"
    )
    
    # Preview
    preview = "⚡ **TOP 10:**\n" + "\n".join([
        f"{i}. `{h[:50]}...`" for i, h in enumerate(hits[:10], 1)
    ])
    await app.send_message(chat_id, preview, parse_mode="Markdown")

PublicDorkBot.send_hits = send_hits

# Files menu (same as before)
@app.on_callback_query(filters.regex(r"^files$"))
async def files_menu(client, query):
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("📄 All Hits", callback_data="hits_all")],
        [InlineKeyboardButton("🧹 Clean", callback_data="clean")]
    ])
    await query.edit_message_text("📁 **Public Files**", reply_markup=kb)

@app.on_callback_query(filters.regex(r"^(hits_all|clean)$"))
async def file_ops(client, query):
    if query.data == "hits_all":
        for f in Path("/root/telegram_files").glob("public_hits_*"):
            await client.send_document(query.message.chat.id, str(f))
    else:
        count = sum(1 for f in Path("/root/telegram_files").glob("*") if f.unlink())
        await query.answer(f"🧹 {count} cleaned")

async def main():
    print("🚀 PUBLIC DorkBot v4 starting...")
    await app.start()
    print("✅ PUBLIC BOT LIVE!")
    await idle()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
