# scripts/run_pipeline.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from video_uploads.upload_video import upload_video
from extracted_faces.extract_faces import extract_faces_from_video
from filter_scripts.filter_unique_faces import filter_unique_faces

from firebase_updates.push_to_firebase import initialize_firebase, mark_attendance

# Set up base paths
BASE = os.path.dirname(os.path.dirname(__file__))

# Paths
video_filename = "test_video.mp4"  # your video file name
video_path = os.path.join(BASE, "video_uploads", video_filename)
faces_dir = os.path.join(BASE, "extracted_faces")
unique_dir = os.path.join(BASE, "unique_faces")
student_dir = os.path.join(BASE, "student_dataset")
haar_path = os.path.join(BASE, "models", "haarcascade_frontalface_default.xml")
firebase_cred = os.path.join(BASE, "firebase_updates", "service_account.json")


# Pipeline Execution
try:
    print("[STEP 1] Loading video...")
    video_file = upload_video(video_path)

    print("[STEP 2] Extracting faces...")
    extract_faces_from_video(video_file, faces_dir, haar_path)

    print("[STEP 3] Filtering unique faces...")
    filter_unique_faces(faces_dir, unique_dir)

    print("[STEP 4] Pushing to Firebase...")
    initialize_firebase(firebase_cred)
    mark_attendance(unique_dir, student_dir)

    print("[✅] Attendance pipeline completed successfully.")

except Exception as e:
    print(f"[❌ ERROR] {str(e)}")
