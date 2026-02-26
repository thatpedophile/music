import os
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from pytgcalls import PyTgCalls, idle
from pytgcalls.types import AudioPiped

# --- CONFIGURATION ---
API_ID = 24344412  # Get from my.telegram.org
API_HASH = "55bc889a002726d80e5c2061c2fd6303"
BOT_TOKEN = "8098076126:AAF-RwYSqM7QpyKdFbou7pyxxobMqGIJhDk"
# The URL where you hosted your index.html on Vercel
WEBAPP_URL = "https://your-vercel-link.vercel.app" 

# --- INITIALIZATION ---
# We use one client for the bot and one for the user account (required for voice chats)
app = Client("music_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
call_py = PyTgCalls(app)

# --- BOT COMMANDS ---

@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    """Sends a button to open the Mini App"""
    await message.reply_text(
        "👋 Welcome! Click the button below to open the Music Player.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Open Music App", web_app=WebAppInfo(url=WEBAPP_URL))]
        ])
    )

@app.on_message(filters.command("play") & filters.group)
async def play_command(client, message):
    """Joins voice chat and plays a sample stream"""
    chat_id = message.chat.id
    # Example stream URL (you can replace this with yt-dlp logic later)
    audio_url = "http://docs.evostream.com/sample_content/assets/sintel1m720p.mp4"
    
    try:
        await call_py.play(chat_id, AudioPiped(audio_url))
        await message.reply_text("🎶 Started streaming in Voice Chat!")
    except Exception as e:
        await message.reply_text(f"Error: {e}")

# --- WEB APP DATA HANDLER ---

@app.on_message(filters.service & filters.group)
async def handle_webapp_data(client, message):
    """Listens for data sent from the Mini App via tg.sendData()"""
    if message.web_app_data:
        data = message.web_app_data.data
        chat_id = message.chat.id

        if data == "/pause":
            await call_py.pause_stream(chat_id)
            await message.reply_text("⏸ Paused via App")
        
        elif data == "/resume":
            await call_py.resume_stream(chat_id)
            await message.reply_text("▶️ Resumed via App")
            
        elif data == "/skip":
            # Add your queue skipping logic here
            await message.reply_text("⏭ Skipped via App")

# --- START THE BOT ---
async def main():
    await call_py.start()
    print("Bot is running...")
    await idle()

if __name__ == "__main__":
    app.run(main())
