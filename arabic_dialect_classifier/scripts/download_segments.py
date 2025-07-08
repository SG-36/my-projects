import os
import subprocess

# ======== CONFIG ========
SEGMENTS_FILE = "data/ADI17/train/segments"
UTT2LANG_FILE = "data/ADI17/train/utt2lang"
OUTPUT_DIR = "data/clips"
DOWNLOAD_DIR = "data/full_videos"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# ======== LOAD LABELS ========
utt2lang = {}
with open(UTT2LANG_FILE, "r") as f:
    for line in f:
        utt_id, lang = line.strip().split()
        utt2lang[utt_id] = lang

# ======== LOAD SEGMENTS ========
segments = []
with open(SEGMENTS_FILE, "r") as f:
    for line in f:
        utt_id, youtube_id, start, end = line.strip().split()
        if utt_id in utt2lang:
            segments.append({
                "utt_id": utt_id,
                "youtube_id": youtube_id,
                "start": float(start),
                "end": float(end),
                "lang": utt2lang[utt_id]
            })

# ======== PROCESS SEGMENTS ========
downloaded = set()

for seg in segments[:50]:  # limit for testing; remove slice to process all
    yid = seg["youtube_id"]
    video_path = os.path.join(DOWNLOAD_DIR, f"{yid}.mp4")
    clip_path = os.path.join(OUTPUT_DIR, f"{seg['utt_id']}_{seg['lang']}.wav")

    # Download full video once
    if yid not in downloaded and not os.path.exists(video_path):
        print(f"\n🔽 Downloading: {yid}")
        result = subprocess.run([
            "yt-dlp", "-f", "bestaudio[ext=mp4]",
            f"https://www.youtube.com/watch?v={yid}",
            "-o", video_path
        ])
        if result.returncode != 0 or not os.path.exists(video_path):
            print(f"❌ Failed to download {yid}")
            continue
        downloaded.add(yid)

    # Cut the segment
    start = seg["start"]
    duration = seg["end"] - seg["start"]
    print(f"✂️  Cutting segment {seg['utt_id']} ({seg['lang']})")

    try:
        subprocess.run([
            "ffmpeg", "-y",
            "-i", video_path,
            "-ss", str(start),
            "-t", str(duration),
            "-ar", "16000", "-ac", "1",  # 16kHz mono
            "-vn",  # no video
            clip_path
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"❌ Failed to segment {seg['utt_id']}: {e}")
        continue

print("\n✅ Done extracting segments.")
