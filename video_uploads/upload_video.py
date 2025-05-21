# video_uploads/upload_video.py
import os

def upload_video(video_path="video_uploads/sample_video.mp4"):
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"[ERROR] Video file not found at path: {video_path}")
    
    print(f"[INFO] Video successfully loaded from: {video_path}")
    return video_path
