# unique_faces/filter_unique_faces.py
import face_recognition
import os
import shutil

def filter_unique_faces(input_dir='extracted_faces', output_dir='unique_faces', tolerance=0.5):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    known_encodings = []
    image_paths = sorted([
        os.path.join(input_dir, f)
        for f in os.listdir(input_dir)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ])

    unique_count = 0
    for img_path in image_paths:
        image = face_recognition.load_image_file(img_path)
        encodings = face_recognition.face_encodings(image)

        if len(encodings) == 0:
            continue

        current_encoding = encodings[0]
        results = face_recognition.compare_faces(known_encodings, current_encoding, tolerance=tolerance)

        if not any(results):
            known_encodings.append(current_encoding)
            new_path = os.path.join(output_dir, f'unique_{unique_count}.jpg')
            shutil.copy(img_path, new_path)
            unique_count += 1
