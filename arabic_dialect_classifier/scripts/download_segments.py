import os
import subprocess
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict

# ======== CONFIG ========
SEGMENTS_FILE = "data/raw_repo/data/train/segments"
UTT2LANG_FILE = "data/raw_repo/data/train/utt2lang"
OUTPUT_DIR = "data/clips"
DOWNLOAD_DIR = "data/full_videos"
COOKIES_FILE = "cookies.txt"
MAX_WORKERS = 5  # Adjust for more/less parallelism

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# ======== LOAD LABELS ========
utt2lang = {}
with open(UTT2LANG_FILE, "r") as f:
    for line in f:
        video_id, lang = line.strip().split()
        utt2lang[video_id] = lang

# ======== LOAD SEGMENTS & GROUP BY VIDEO ========
segments_by_video = defaultdict(list)
with open(SEGMENTS_FILE, "r") as f:
    for line in f:
        utt_id, youtube_id, start, end = line.strip().split()
        lang = utt2lang.get(youtube_id, "unknown")
        segments_by_video[youtube_id].append({
            "utt_id": utt_id,
            "youtube_id": youtube_id,
            "start": float(start),
            "end": float(end),
            "lang": lang
        })

print(f"Loaded {len(segments_by_video)} videos")
print(f"Total segments: {sum(len(v) for v in segments_by_video.values())}")

# ======== VIDEO PROCESSING FUNCTION ========
def process_video(yid, segs):
    video_path = os.path.join(DOWNLOAD_DIR, f"{yid}.mp4")

    # ----- Download -----
    if not os.path.exists(video_path):
        cmd = [
            "yt-dlp", "-f", "bestaudio[ext=mp4]",
            f"https://www.youtube.com/watch?v={yid}",
            "-o", video_path
        ]
        if os.path.exists(COOKIES_FILE):
            cmd.insert(1, "--cookies")
            cmd.insert(2, COOKIES_FILE)

        result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        if result.returncode != 0 or not os.path.exists(video_path):
            print(f"❌ Failed to download {yid}")
            with open("failed_downloads.log", "a") as log:
                log.write(f"{yid}\n")
            return

    # ----- Extract segments -----
    for seg in segs:
        clip_path = os.path.join(OUTPUT_DIR, f"{seg['utt_id']}_{seg['lang']}.wav")
        start = seg["start"]
        duration = seg["end"] - seg["start"]

        try:
            subprocess.run([
                "ffmpeg", "-y", "-i", video_path,
                "-ss", str(start), "-t", str(duration),
                "-ar", "16000", "-ac", "1", "-vn", clip_path
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception as e:
            print(f"❌ Segment failed {seg['utt_id']}: {e}")
            continue

    # ----- Delete full video -----
    if os.path.exists(video_path):
        os.remove(video_path)

# ======== PARALLEL EXECUTION ========
with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    futures = [executor.submit(process_video, yid, segs) for yid, segs in segments_by_video.items()]

    for future in tqdm(as_completed(futures), total=len(futures), desc="Processing videos"):
        future.result()

print("\n✅ All done.")
