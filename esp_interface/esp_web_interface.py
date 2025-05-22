from flask import Flask
import threading
import time
import random
import datetime
import subprocess
import cv2
import requests
from firebase_admin import credentials, initialize_app, db



cred = credentials.Certificate('../firebase_updates/service_account.json')
initialize_app(cred, {
    'databaseURL': 'Your firebase project database URL'
})


app = Flask(__name__)

ESP32_URL = " Your ESP32 camera IP" 
VIDEO_PATH = "video_uploads/test_video.mp4"

def push_random_time():
    now = datetime.datetime.now()
    rand_minute = random.randint(1, 5)
    future_time = now + datetime.timedelta(minutes=rand_minute)
    time_str = future_time.strftime("%H:%M:%S")

    db.reference("rooms/A1").set(time_str)
    print(f"[FIREBASE] Random time {time_str} pushed to rooms/A1")

    return future_time


def wait_for_camera_online():
    print("[CAMERA] Waiting for ESP32 camera to come online...")
    while True:
        cap = cv2.VideoCapture(ESP32_URL)
        if cap.isOpened():
            print("[CAMERA] ESP32 is online.")
            cap.release()
            break
        else:
            print("[CAMERA] Not online. Retrying...")
        time.sleep(2)


def record_video():
    print("[VIDEO] Starting 1-minute recording...")
    cap = cv2.VideoCapture(ESP32_URL)
    if not cap.isOpened():
        print("[ERROR] Unable to open camera stream.")
        return

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(VIDEO_PATH, fourcc, 20.0, (640, 480))  

    start_time = time.time()
    while int(time.time() - start_time) < 60:
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Frame not captured.")
            break
        out.write(frame)

    cap.release()
    out.release()
    print("[VIDEO] Recording complete. Saved to", VIDEO_PATH)


def run_pipeline():
    print("[PIPELINE] Starting face recognition...")
    subprocess.call(["python", "scripts/run_pipeline.py"])


def scheduled_task():
    future_time = push_random_time()
    wait_seconds = (future_time - datetime.datetime.now()).total_seconds()
    print(f"[WAIT] Sleeping for {int(wait_seconds)} seconds until target time...")
    time.sleep(max(0, wait_seconds))

    wait_for_camera_online()
    record_video()
    run_pipeline()


@app.route('/')
def index():
    threading.Thread(target=scheduled_task).start()
    return "ESP32 Interface Loaded. Attendance Process Started."


if __name__ == '__main__':
    app.run(debug=True)
