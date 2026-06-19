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


def get_undertone(image, face):

    x, y, w, h = face

    # Sample cheek/forehead area only — avoids eyes, lips,
    # nostrils, hair and background pixels at bounding box edges
    face_region = image[
        y + h//4 : y + h//2,
        x + w//4 : x + 3*w//4
    ]

    if face_region.size == 0:
        face_region = image[y:y+h, x:x+w]

    avg_color = np.mean(face_region, axis=(0, 1))

    # Convert to LAB color space.
    # LAB b-channel = yellow-blue axis, a-channel = red-green axis.
    # warmth_score = b - a reliably separates warm (golden/yellow)
    # from cool (pink/rosy) skin — unlike raw RGB where skin pixels
    # are always red-dominant regardless of actual undertone.
    sample = np.uint8([[avg_color]])
    lab = cv2.cvtColor(sample, cv2.COLOR_BGR2LAB)[0][0]

    a_channel = float(lab[1]) - 128.0
    b_channel = float(lab[2]) - 128.0
    warmth_score = b_channel - a_channel

    if warmth_score > 4:
        return "Warm"
    elif warmth_score < -4:
        return "Cool"
    else:
        return "Neutral"


def get_skin_tone(image, face):

    x, y, w, h = face

    face_roi = image[
        y + h//5 : y + 4*h//5,
        x + w//5 : x + 4*w//5
    ]

    if face_roi.size == 0:
        return "Medium"

    avg_color = np.mean(face_roi, axis=(0, 1))
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


def get_hair_color(image, face):

    x, y, w, h = face

    hair_roi = image[
        max(0, y - h//3) : y,
        x : x + w
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
