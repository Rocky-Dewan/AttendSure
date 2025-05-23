# firebase_updates/push_to_firebase.py
import face_recognition
import os
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime 

def initialize_firebase(cred_path):
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred, {
        'databaseURL': ''  # Replace this with your DB URL
    })

def load_student_encodings(student_dir):
    encodings = {}
    for file in os.listdir(student_dir):
        if file.endswith(".jpg"):
            path = os.path.join(student_dir, file)
            img = face_recognition.load_image_file(path)
            encoding = face_recognition.face_encodings(img)
            if encoding:
                student_id, name = file.replace(".jpg", "").split("_", 1)
                encodings[(student_id, name)] = encoding[0]
    return encodings

def mark_attendance(unique_faces_dir, student_dir, course_code="CSE425"):
    students = load_student_encodings(student_dir)
    marked = set()

    today_date = datetime.now().strftime("%Y-%m-%d")
    attendance_path = f'attendance/{course_code}/{today_date}'

    for file in os.listdir(unique_faces_dir):
        if not file.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue

        path = os.path.join(unique_faces_dir, file)
        unknown_img = face_recognition.load_image_file(path)
        unknown_encodings = face_recognition.face_encodings(unknown_img)

        if not unknown_encodings:
            continue

        for (student_id, name), known_encoding in students.items():
            match = face_recognition.compare_faces([known_encoding], unknown_encodings[0], tolerance=0.5)
            if match[0] and student_id not in marked:
                marked.add(student_id)

                # ✅ Push to "attendance"
                db.reference(f'{attendance_path}/{student_id}').set({
                    'attendance': 1
                })

                # ✅ Push to "student"
                db.reference(f'student/{student_id}').set({
                    'name': name,
                    'image': f"{student_id}_{name}.jpg",
                    'password': '1234'
                })

                print(f"✅ Marked {student_id} ({name}) as present.")

    # ✅ Mark absent students
    for student_id, name in students.keys():
        if student_id not in marked:
            db.reference(f'{attendance_path}/{student_id}').set({
                'attendance': 0
            })

            # Ensure student info is still pushed
            db.reference(f'student/{student_id}').set({
                'name': name,
                'image': f"{student_id}_{name}.jpg",
                'password': '1234'
            })

            print(f"❌ Marked {student_id} ({name}) as absent.")
