import os
import re
from pathlib import Path
from typing import Optional, Tuple, Dict, Any

import requests
import soundcloud
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from ZeMusic.utils.formatters import seconds_to_min
from ZeMusic import app  # Make sure "ZeMusic" is your project name or you import app correctly
from ZeMusic.plugins.play.filters import command

# SoundCloud credentials
SOUNDCLOUD_CLIENT_ID = os.environ.get("SOUNDCLOUD_CLIENT_ID")  # Get from environment variables

if not SOUNDCLOUD_CLIENT_ID:
    raise ValueError("SOUNDCLOUD_CLIENT_ID environment variable not set.")

# Initialize SoundCloud client
sc_client = soundcloud.Client(client_id=SOUNDCLOUD_CLIENT_ID)

channel = "KHAYAL70"  # Your channel username
lnk = "https://t.me/" + config.CHANNEL_LINK
Nem = config.BOT_NAME + " ابحث"

def remove_if_exists(path):
    # ... (same as before)

async def download_file(url: str, filename: str):
    """Helper function to download files asynchronously."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                f = await aiofiles.open(filename, mode= wb )
                await f.write(await resp.read())
                await f.close()
            else:
                raise Exception(f"Could not download file: {resp.status}")

async def search_and_download_soundcloud(query: str) -> Tuple[Optional[str], Optional[str], Optional[Dict]]:
    """Searches SoundCloud and downloads the track."""
    try:
        tracks = sc_client.get( /tracks , q=query, limit=1)
        if not tracks:
            return None, None, None

        track = tracks[0]
        title = track.title[:40]
        title = re.sub(r"[\\/*?\"<>|]", "", title)

        filename = f"{title}.mp3"

        # Download artwork asynchronously
        artwork_url = track.artwork_url or track.user[ avatar_url ]
        thumb_name = None # Initialize
        if artwork_url:
            thumb_name = f"thumb{title}.jpg"
            try:
              await download_file(artwork_url, thumb_name)
            except: # Handle exceptions
              thumb_name = None

        with open(filename, "wb+") as file:
            track.write_mp3_to(file) # Write track to file

        track_details = {
            "title": track.title,
            "duration_sec": track.duration / 1000,
            "duration_min": seconds_to_min(track.duration / 1000),
            "uploader": track.user["username"],
            "filepath": filename,
        }
        return filename, thumb_name, track_details

    except Exception as e:
        print(f"Error during SoundCloud search and download: {e}")
        return None, None, None



@app.on_message(command(["song","/song", "بحث",Nem]))
async def song_downloader(client: Client, message: Message):
    query = " ".join(message.command[1:])
    m = await message.reply_text("<b>⇜ جـارِ البحث عـن المقطـع الصـوتـي . . .</b>")

    audio_file, thumb_name, info_dict = await search_and_download_soundcloud(query)

    if not audio_file:
        await m.edit("- لم يتم العثـور على نتائج ؟!\n- حـاول مجـدداً . . .")
        return

    await m.edit("<b>⇜ جـارِ التحميل ▬▭ . . .</b>")
    # Use info_dict from SoundCloud
    rep = f"ᴍʏ ᴡᴏʀʟᴅ 𓏺 @{channel} "
    host = str(info_dict["uploader"])
    dur = int(info_dict["duration_sec"]) # Use duration_sec from info_dict directly
    await m.edit("<b>⇜ جـارِ التحميل ▬▬ . . .</b>")

    try:
        await message.reply_audio(
           audio=audio_file,
           caption=rep,
           title=info_dict[ title ], #Use title from info_dict
           performer=host,
           thumb=thumb_name,
           duration=dur,
           # ... your reply markup
        )
        await m.delete()
        remove_if_exists(audio_file)
        if thumb_name:
            remove_if_exists(thumb_name)

    except Exception as e:
        await m.edit(f"Error sending audio: {e}")



# ... (Remove or adapt the video_search function as needed)
