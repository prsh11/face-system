import cv2
from deepface import DeepFace
from retinaface import RetinaFace

vid = cv2.VideoCapture(0)


def compare_face(img):
    return DeepFace.find(img, "./images")


while True:

    ret, frame = vid.read()

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

    res = RetinaFace.detect_faces(frame)
    for face in res.keys():
        f = res[face]
        area = f["facial_area"]

        cv2.rectangle(frame, (area[2], area[3]), (area[0], area[1]), (255, 255, 255), 1)
    cv2.imshow("frame", frame)


vid.release()
cv2.destroyAllWindows()
