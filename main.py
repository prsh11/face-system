import face_recognition
import cv2
import numpy as np
import os
from datetime import datetime
from database import Database

dat = Database("db.sqlite")
video_capture = cv2.VideoCapture(0)

today_date = datetime.now().date().strftime("%Y/%m/%d")

known_face_encodings = []

known_face_names = []

for file in os.listdir("images"):
    image = face_recognition.load_image_file(f"images/{file}")
    encoding = face_recognition.face_encodings(image)[0]
    known_face_encodings.append(encoding)
    known_face_names.append(int(file.split(".jpg")[0]))


face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    ret, frame = video_capture.read()

    if process_this_frame:
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(
            rgb_small_frame, face_locations
        )

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(
                known_face_encodings, face_encoding
            )
            id = -1

            face_distances = face_recognition.face_distance(
                known_face_encodings, face_encoding
            )
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                id = known_face_names[best_match_index]

            name = dat.get_data(id)[1] if id != -1 else "Unknown"
            face_names.append(name)
            if id != -1:
                dat.insert_record(id, today_date)

    process_this_frame = not process_this_frame

    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        cv2.rectangle(
            frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED
        )
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    cv2.imshow("Video", frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video_capture.release()
cv2.destroyAllWindows()
