import os
import re
import sys
import m3u8
import json
import time
import pytz
import asyncio
import requests
import subprocess
import urllib
import urllib.parse
import yt_dlp
import tgcrypto
import cloudscraper
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from base64 import b64encode, b64decode
from logs import logging
from bs4 import BeautifulSoup
import saini as helper
from utils import progress_bar
from vars import API_ID, API_HASH, BOT_TOKEN, OWNER, CREDIT
from aiohttp import ClientSession
from subprocess import getstatusoutput
from pytube import YouTube
from aiohttp import web
import random
from pyromod import listen
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import aiohttp
import aiofiles
import zipfile
import shutil
import ffmpeg

# Initialize the bot
bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

AUTH_USER = os.environ.get('AUTH_USERS', '7527795504').split(',')
# Add More AUTH_USER
AUTH_USER.append('5680454765')
AUTH_USERS = [int(user_id) for user_id in AUTH_USER]
if int(OWNER) not in AUTH_USERS:
    AUTH_USERS.append(int(OWNER))
CHANNEL_OWNERS = {}
CHANNELS = os.environ.get('CHANNELS', '').split(',')
CHANNELS_LIST = [int(channel_id) for channel_id in CHANNELS if channel_id.isdigit()]
cookies_file_path = os.getenv("cookies_file_path", "youtube_cookies.txt")
api_url = "http://master-api-v3.vercel.app/"
api_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNzkxOTMzNDE5NSIsInRnX3VzZXJuYW1lIjoi4p61IFtvZmZsaW5lXSIsImlhdCI6MTczODY5MjA3N30.SXzZ1MZcvMp5sGESj0hBKSghhxJ3k1GTWoBUbivUe1I"
token_cp ='eyJjb3Vyc2VJZCI6IjQ1NjY4NyIsInR1dG9ySWQiOm51bGwsIm9yZ0lkIjo0ODA2MTksImNhdGVnb3J5SWQiOm51bGx9r'
adda_token = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJkcGthNTQ3MEBnbWFpbC5jb20iLCJhdWQiOiIxNzg2OTYwNSIsImlhdCI6MTc0NDk0NDQ2NCwiaXNzIjoiYWRkYTI0Ny5jb20iLCJuYW1lIjoiZHBrYSIsImVtYWlsIjoiZHBrYTU0NzBAZ21haWwuY29tIiwicGhvbmUiOiI3MzUyNDA0MTc2IiwidXNlcklkIjoiYWRkYS52MS41NzMyNmRmODVkZDkxZDRiNDkxN2FiZDExN2IwN2ZjOCIsImxvZ2luQXBpVmVyc2lvbiI6MX0.0QOuYFMkCEdVmwMVIPeETa6Kxr70zEslWOIAfC_ylhbku76nDcaBoNVvqN4HivWNwlyT0jkUKjWxZ8AbdorMLg"
photologo = 'https://tinypic.host/images/2025/05/29/Medusaxd-Bot_20250529_184235_0000.png' #https://envs.sh/GV0.jpg
photoyt = 'https://tinypic.host/images/2025/03/18/YouTube-Logo.wine.png' #https://envs.sh/GVi.jpg
photocp = 'https://tinypic.host/images/2025/03/28/IMG_20250328_133126.jpg'
photozip = 'https://envs.sh/cD_.jpg'

# Authorization decorator
def authorized_users_only(func):
    async def wrapper(client, message, *args, **kwargs):
        if message.from_user.id not in AUTH_USERS:
            name = message.from_user.first_name
            await message.reply_text(
                f"Hello {name}\n\n"
                "Welcome to the Text To Video Extractor Bot! I can help you extract and process videos from various sources.\n"
                "Powered by @medusaXD\n\n"
                "You are not authorized to use this command. Contact my Owner: @medusaXD"
            )
            return
        return await func(client, message, *args, **kwargs)
    return wrapper

async def show_random_emojis(message):
    emojis = ['🐼', '🐶', '🐅', '⚡️', '🚀', '✨', '💥', '☠️', '🥂', '🍾', '📬', '👻', '👀', '🌹', '💀', '🐇', '⏳', '🔮', '🦔', '📖', '🦁', '🐱', '🐻‍❄️', '☁️', '🚹', '🚺', '🐠', '🦋']
    emoji_message = await message.reply_text(' '.join(random.choices(emojis, k=1)))
    return emoji_message

# Inline keyboard for start command
BUTTONSCONTACT = InlineKeyboardMarkup([[InlineKeyboardButton(text="📞 Contact", url="https://t.me/saini_contact_bot")]])
keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="🛠️ Admin", url="https://t.me/medusaXD"),
            InlineKeyboardButton(text="🛠️ Help", url="/help"),
        ],
    ]
)

# Image URLs for the random image feature
image_urls = [
    "https://tinypic.host/images/2025/05/29/Medusaxd-Bot_20250529_184235_0000.png",
    "https://tinypic.host/images/2025/05/29/Medusaxd-Bot_20250529_184235_0000.png",
    # Add more image URLs as needed
]

@bot.on_message(filters.command("start") & filters.private)
async def start_command(client: Client, message: Message):
    name = message.from_user.first_name

    # Random emoji message
    emoji_message = await show_random_emojis(message)

    # Start message with commands list
    if message.from_user.id in AUTH_USERS:
        start_text = f"""Hello {name} 👋

Welcome to the Text To Video Extractor Bot! I can help you extract and process videos from various sources.
Powered by @medusaXD

**Available Commands:**
• `/add_channel` - Add a channel for content distribution
• `/remove_channel` - Remove a channel from distribution list
• `/channels` - List all authorized channels
• `/cookies` - Upload cookies file for authentication

Send me a link to extract content from supported platforms!"""
    else:
        start_text = f"""Hello {name}

Welcome to the Text To Video Extractor Bot! I can help you extract and process videos from various sources.
Powered by @medusaXD

You are not authorized to use this bot. Contact my Owner: @medusaXD"""

    await message.reply_text(start_text, reply_markup=keyboard)
    await emoji_message.delete()

@bot.on_message(filters.command("help") & filters.private)
@authorized_users_only
async def help_command(client: Client, message: Message):
    # Random emoji message
    emoji_message = await show_random_emojis(message)

    help_text = """**📚 Text To Video Extractor Bot Help**

**Main Commands:**
• `/start` - Start the bot
• `/help` - Show this help message
• `/add_channel` - Add a channel for content distribution
• `/remove_channel` - Remove a channel from distribution list
• `/channels` - List all authorized channels
• `/cookies` - Upload cookies file for authentication

**Admin Commands (Owner Only):**
• `/addauth` - Add an authorized user
• `/remauth` - Remove an authorized user
• `/users` - List all authorized users

Send me a link to extract content from supported platforms!"""

    await message.reply_text(help_text, reply_markup=BUTTONSCONTACT)
    await emoji_message.delete()

@bot.on_message(filters.command("addauth") & filters.private)
@authorized_users_only
async def add_auth_user(client: Client, message: Message):
    if message.chat.id != OWNER:
        return await message.reply_text("You are not authorized to use this command.")

    try:
        new_user_id = int(message.command[1])
        if new_user_id in AUTH_USERS:
            await message.reply_text("User ID is already authorized.")
        else:
            AUTH_USERS.append(new_user_id)
            # Update the environment variable (if needed)
            os.environ['AUTH_USERS'] = ','.join(map(str, AUTH_USERS))
            await message.reply_text(f"User ID {new_user_id} added to authorized users.")
    except (IndexError, ValueError):
        await message.reply_text("Please provide a valid user ID.")

@bot.on_message(filters.command("remauth") & filters.private)
@authorized_users_only
async def remove_auth_user(client: Client, message: Message):
    if message.chat.id != OWNER:
        return await message.reply_text("You are not authorized to use this command.")

    try:
        user_id_to_remove = int(message.command[1])
        if user_id_to_remove not in AUTH_USERS:
            await message.reply_text("User ID is not in the authorized users list.")
        else:
            AUTH_USERS.remove(user_id_to_remove)
            # Update the environment variable (if needed)
            os.environ['AUTH_USERS'] = ','.join(map(str, AUTH_USERS))
            await message.reply_text(f"User ID {user_id_to_remove} removed from authorized users.")
    except (IndexError, ValueError):
        await message.reply_text("Please provide a valid user ID.")

@bot.on_message(filters.command("users") & filters.private)
@authorized_users_only
async def list_auth_users(client: Client, message: Message):
    if message.chat.id != OWNER:
        return await message.reply_text("You are not authorized to use this command.")

    user_list = '\n'.join(map(str, AUTH_USERS))
    await message.reply_text(f"<blockquote>Authorized Users:</blockquote>\n{user_list}")

@bot.on_message(filters.command(["add_channel", "addchnl"]) & filters.private)
@authorized_users_only
async def add_channel(client: Client, message: Message):
    try:
        new_channel_id = int(message.command[1])

        # Validate that the channel ID starts with -100
        if not str(new_channel_id).startswith("-100"):
            return await message.reply_text("Invalid channel ID. Channel IDs must start with -100.")

        if new_channel_id in CHANNELS_LIST:
            await message.reply_text("Channel ID is already added.")
        else:
            CHANNELS_LIST.append(new_channel_id)
            CHANNEL_OWNERS[new_channel_id] = message.from_user.id  # Assign the user as the owner of the channel
            # Update the environment variable (if needed)
            os.environ['CHANNELS'] = ','.join(map(str, CHANNELS_LIST))
            await message.reply_text(f"Channel ID {new_channel_id} added to the list and you are now the owner.")
    except (IndexError, ValueError):
        await message.reply_text("Please provide a valid channel ID.")

@bot.on_message(filters.command(["remove_channel", "remchnl"]) & filters.private)
@authorized_users_only
async def remove_channel(client: Client, message: Message):
    try:
        channel_id_to_remove = int(message.command[1])

        # Check if the channel exists in the list
        if channel_id_to_remove not in CHANNELS_LIST:
            return await message.reply_text("Channel ID is not in the list.")

        # Check if the user is the OWNER or the channel owner
        if message.from_user.id != OWNER and CHANNEL_OWNERS.get(channel_id_to_remove) != message.from_user.id:
            return await message.reply_text("You are not authorized to remove this channel.")

        # Remove the channel
        CHANNELS_LIST.remove(channel_id_to_remove)
        if channel_id_to_remove in CHANNEL_OWNERS:
            del CHANNEL_OWNERS[channel_id_to_remove]  # Remove from the ownership dictionary if present

        # Update the environment variable (if needed)
        os.environ['CHANNELS'] = ','.join(map(str, CHANNELS_LIST))
        await message.reply_text(f"Channel ID {channel_id_to_remove} removed from the list.")
    except (IndexError, ValueError):
        await message.reply_text("Please provide a valid channel ID.")

@bot.on_message(filters.command("channels") & filters.private)
@authorized_users_only
async def list_channels(client: Client, message: Message):
    if message.chat.id != OWNER:
        return await message.reply_text("You are not authorized to use this command.")

    if not CHANNELS_LIST:
        await message.reply_text("No channels have been added yet.")
    else:
        channel_list = '\n'.join(map(str, CHANNELS_LIST))
        await message.reply_text(f"<blockquote>Authorized Channels:</blockquote>\n{channel_list}")

@bot.on_message(filters.command("cookies") & filters.private)
@authorized_users_only
async def cookies_handler(client: Client, m: Message):
    await m.reply_text(
        "Please upload the cookies file (.txt format).",
        quote=True
    )

    try:
        # Wait for the user to send the cookies file
        input_message: Message = await client.listen(m.chat.id)

        # Validate the uploaded file
        if not input_message.document or not input_message.document.file_name.endswith(".txt"):
            await m.reply_text("Invalid file type. Please upload a .txt file.")
            return

        # Download the cookies file
        downloaded_path = await input_message.download()

        # Read the content of the uploaded file
        # This part was incomplete in the original code

        # Save the cookies file
        with open(cookies_file_path, 'w') as f:
            with open(downloaded_path, 'r') as uploaded:
                f.write(uploaded.read())

        await m.reply_text("Cookies file uploaded successfully!")

        # Clean up the temporary file
        if os.path.exists(downloaded_path):
            os.remove(downloaded_path)

    except Exception as e:
        await m.reply_text(f"An error occurred: {str(e)}")
