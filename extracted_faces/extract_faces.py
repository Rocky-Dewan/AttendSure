# extracted_faces/extract_faces.py
import cv2
import os

def extract_faces_from_video(video_path, output_dir, haar_path):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    face_cascade = cv2.CascadeClassifier(haar_path)
    cap = cv2.VideoCapture(video_path)

    frame_count = 0
    face_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            face = frame[y:y+h, x:x+w]
            face_path = os.path.join(output_dir, f"face_{face_count}.jpg")
            cv2.imwrite(face_path, face)
            face_count += 1

    cap.release()
    print(f"Extracted {face_count} faces from {frame_count} frames.")
