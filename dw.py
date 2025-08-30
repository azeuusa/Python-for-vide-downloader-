import os
import subprocess
import sys
from urllib.parse import urlparse

def clear():
    os.system("clear" if os.name == "posix" else "cls")

def banner():
    print(r"""
 /$$   /$$ /$$$$$$$$  /$$$$$$   /$$$$$$  /$$$$$$$$
| $$  / $$|_____ $$  /$$__  $$ /$$__  $$| $$_____/
|  $$/ $$/     /$$/ | $$  \ $$| $$  \ $$| $$      
 \  $$$$/     /$$/  | $$$$$$$$| $$$$$$$$| $$$$$   
  >$$  $$    /$$/   | $$__  $$| $$__  $$| $$__/   
 /$$/\  $$  /$$/    | $$  | $$| $$  | $$| $$      
| $$  \ $$ /$$$$$$$$| $$  | $$| $$  | $$| $$      
|__/  |__/|________/|__/  |__/|__/  |__/|__/      
                                                  
                                                  
                                                  

     Multi Downloader by xzaaftry
      [YT | TikTok | IG | FB]
    """)

def ask_yes_no(prompt):
    while True:
        answer = input(f"{prompt} (y/n): ").lower()
        if answer in ("y", "n"):
            return answer == "y"
        print("⚠️ Masukkan hanya 'y' atau 'n'.")

def detect_platform(url):
    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    path = parsed.path.lower()

    if "tiktok.com" in domain:
        return "tiktok"
    elif "youtube.com" in domain or "youtu.be" in domain:
        return "youtube"
    elif "instagram.com" in domain and ("/reel/" in path or "/p/" in path):
        return "instagram"
    elif "facebook.com" in domain or "fb.watch" in domain:
        return "facebook"
    else:
        return "unknown"

def choose_youtube_resolution():
    print("\n📺 Pilih resolusi video:")
    print("1. 144p")
    print("2. 360p")
    print("3. 720p")
    print("4. 1080p")
    print("5. Best quality")
    choice = input("Pilih (1-5): ").strip()

    mapping = {
        "1": "bv[height=144]+ba/b[height=144]",
        "2": "bv[height=360]+ba/b[height=360]",
        "3": "bv[height=720]+ba/b[height=720]",
        "4": "bv[height=1080]+ba/b[height=1080]",
        "5": "best"
    }
    return mapping.get(choice, "best")

def download_video(url, platform, quality="best"):
    if platform == "tiktok":
        out_template = "/sdcard/Download/TikTok_%(uploader)s_%(id)s.%(ext)s"
        fmt = "bv+ba/b" if quality == "hd" else "best"
    elif platform == "youtube":
        out_template = "/sdcard/Download/YT_%(title).50s.%(ext)s"
        fmt = quality
    elif platform == "instagram":
        out_template = "/sdcard/Download/IG_%(title).50s.%(ext)s"
        fmt = "best"
    elif platform == "facebook":
        out_template = "/sdcard/Download/FB_%(id)s.%(ext)s"
        fmt = "best"
    else:
        print("❌ Platform tidak dikenali.")
        return

    command = [
        "yt-dlp",
        "-f", fmt,
        "--merge-output-format", "mp4",
        "--no-playlist",
        "-o", out_template,
        url
    ]

    try:
        print(f"\n🚀 Mengunduh dari {platform.upper()}...\n")
        subprocess.run(command, check=True)
        print(f"\n✅ Selesai! File disimpan di folder Download Android.")
    except subprocess.CalledProcessError:
        print("❌ Terjadi kesalahan saat mengunduh.")

def download_youtube_mp3(url):
    out_template = "/sdcard/Download/YT_%(title).50s.%(ext)s"
    command = [
        "yt-dlp",
        "-x",
        "--audio-format", "mp3",
        "--no-playlist",
        "-o", out_template,
        url
    ]
    try:
        print("\n🎧 Mengunduh audio MP3 dari YouTube...\n")
        subprocess.run(command, check=True)
        print("✅ MP3 berhasil disimpan di folder Download Android.")
    except subprocess.CalledProcessError:
        print("❌ Gagal download MP3 dari YouTube.")

def download_tiktok_mp3(url):
    out_template = "/sdcard/Download/TikTok_Audio_%(uploader)s_%(id)s.%(ext)s"
    command = [
        "yt-dlp",
        "-x",
        "--audio-format", "mp3",
        "--no-playlist",
        "--quiet",
        "--no-warnings",
        "-o", out_template,
        url
    ]
    try:
        print("\n🎶 Mengunduh audio (lagu) dari TikTok...\n")
        subprocess.run(command, check=True)
        print("✅ Audio berhasil disimpan di folder Download Android.")
    except subprocess.CalledProcessError:
        print("❌ Gagal mengunduh audio dari TikTok.")

def main():
    while True:
        clear()
        banner()
        print("Ketik 'exit' untuk keluar dari program.")
        url = input("🔗 Masukkan URL (TikTok / YouTube / IG / FB): ").strip()

        if url.lower() == "exit":
            print("👋 Terima kasih sudah menggunakan downloader ini.")
            sys.exit(0)

        platform = detect_platform(url)

        if platform == "unknown":
            print("❌ URL tidak dikenali. Pastikan format link valid.")
            input("\nTekan Enter untuk lanjut...")
            continue

        if not ask_yes_no(f"❓ Mulai download dari {platform.upper()}?"):
            print("⛔ Dibatalkan.")
            input("\nTekan Enter untuk lanjut...")
            continue

        if platform == "youtube":
            print("\n🎥 Pilih mode:")
            print("1. Video (pilih resolusi)")
            print("2. Audio MP3")
            mode = input("Pilih (1/2): ").strip()

            if mode == "2":
                download_youtube_mp3(url)
            else:
                resolution = choose_youtube_resolution()
                download_video(url, platform, quality=resolution)

        elif platform == "tiktok":
            if ask_yes_no("🎵 Ingin download sebagai lagu/audio saja?"):
                download_tiktok_mp3(url)
            else:
                is_hd = ask_yes_no("📽️ Ingin kualitas HD?")
                download_video(url, platform, quality="hd" if is_hd else "best")
        else:
            download_video(url, platform)

        input("\n🔄 Tekan Enter untuk kembali ke menu...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n❌ Dibatalkan oleh pengguna.")
        sys.exit(0)