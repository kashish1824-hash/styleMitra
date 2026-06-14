import cv2
import numpy as np


def detect_face(image_path):

    image = cv2.imread(image_path)

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    face_detector = cv2.CascadeClassifier(
        cv2.data.haarcascades +
        "haarcascade_frontalface_default.xml"
    )

    faces = face_detector.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=8,
        minSize=(100, 100)
    )

    return image, faces


def get_undertone(
    image,
    face
):

    x, y, w, h = face

    face_region = image[
        y:y+h,
        x:x+w
    ]

    avg_color = np.mean(
        face_region,
        axis=(0, 1)
    )

    blue = avg_color[0]
    red = avg_color[2]

    if red > blue + 20:
        return "Warm"

    elif blue > red + 20:
        return "Cool"

    else:
        return "Neutral"


def get_skin_tone(
    image,
    face
):

    x, y, w, h = face

    face_roi = image[
        y + h//5:y + 4*h//5,
        x + w//5:x + 4*w//5
    ]

    if face_roi.size == 0:
        return "Medium"

    avg_color = np.mean(
        face_roi,
        axis=(0, 1)
    )

    brightness = np.mean(avg_color)

    if brightness > 190:
        return "Very Fair"

    elif brightness > 165:
        return "Fair"

    elif brightness > 140:
        return "Medium"

    elif brightness > 115:
        return "Brown"

    elif brightness > 90:
        return "Dark"

    else:
        return "Very Dark"


def get_hair_color(
    image,
    face
):

    x, y, w, h = face

    hair_roi = image[
        max(0, y - h//3):y,
        x:x+w
    ]

    if hair_roi.size == 0:
        return "Black"

    brightness = np.mean(hair_roi)

    if brightness < 120:
        return "Black"

    elif brightness < 170:
        return "Dark Brown"

    else:
        return "Brown"