from fastapi import FastAPI, HTTPException
import yt_dlp
import os

app = FastAPI()

# Cookies file ka path define karein (Aapki main.py ke sath hi cookies.txt honi chahiye)
COOKIES_FILE = "cookies.txt"

# 1. Home Route - Connection check karne ke liye
@app.get("/")
def home():
    return {"status": "Online", "message": "API is ready!"}

# 2. Download Route - Android App is se link mangwaye gi
@app.get("/download")
def get_reel_url(url: str):
    try:
        # URL se faltu brackets saaf karna (Lekin query parameters ko delete nahi karna, Instagram ke liye zaroori hain)
        clean_url = url.strip().replace('[', '').replace(']', '')
        
        # yt_dlp configuration
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
        }
        
        # Agar cookies.txt file maujood hai, to usko use karein
        if os.path.exists(COOKIES_FILE):
            ydl_opts['cookiefile'] = COOKIES_FILE
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Video information extract karna
            info = ydl.extract_info(clean_url, download=False)
            video_url = info.get('url')
            
            # Agar URL mil jaye to JSON response bhejna
            if video_url:
                return {
                    "status": "success",
                    "download_url": video_url
                }
            else:
                return {"status": "error", "message": "Could not find video URL"}
            
    except Exception as e:
        # Agar koi error aaye (jaise invalid link ya login issue)
        return {"status": "error", "message": str(e)}
