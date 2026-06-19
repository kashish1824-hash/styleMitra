import cv2
import numpy as np


def detect_face(image_path):

    image = cv2.imread(image_path)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    face_detector = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    faces = face_detector.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=8,
        minSize=(100, 100)
    )

    return image, faces


def _skin_mask(region_bgr):
    """
    Return a boolean mask of skin pixels using two HSV ranges.
    Range 1 covers standard skin (warm/medium/dark).
    Range 2 covers fair/rosy/pink skin that has higher hue.
    Using two ranges instead of one wide range avoids letting
    non-skin warm colours (orange objects, brown walls) through.
    """
    hsv = cv2.cvtColor(region_bgr, cv2.COLOR_BGR2HSV)

    # Range 1: standard skin — covers medium/dark/warm tones
    lower1 = np.array([0,  20, 70],  dtype=np.uint8)
    upper1 = np.array([20, 180, 255], dtype=np.uint8)
    mask1 = cv2.inRange(hsv, lower1, upper1)

    # Range 2: fair/rosy/pink skin — slightly higher hue, lower sat
    lower2 = np.array([0,  10, 140], dtype=np.uint8)
    upper2 = np.array([25, 100, 255], dtype=np.uint8)
    mask2 = cv2.inRange(hsv, lower2, upper2)

    return cv2.bitwise_or(mask1, mask2)


def _avg_lab_masked(region_bgr, mask):
    """
    Average LAB color of pixels where mask > 0.
    Falls back to unmasked average if too few skin pixels found.
    """
    lab = cv2.cvtColor(region_bgr, cv2.COLOR_BGR2LAB)
    skin_pixels = lab[mask > 0]

    if len(skin_pixels) < 30:
        # Too few skin pixels — fall back to full region average
        skin_pixels = lab.reshape(-1, 3)

    return np.mean(skin_pixels, axis=0)


def get_undertone(image, face):
    """
    Detect undertone by:
    1. Sampling three skin zones: forehead, left cheek, right cheek
    2. Masking out non-skin pixels in each zone (eyes, lips, shadows)
    3. Averaging LAB values of skin pixels only
    4. Computing warmth_score = b_channel - a_channel
       b (yellow-blue axis) > a (red-green axis) = Warm
       a > b = Cool
       balanced = Neutral

    LAB is used instead of raw RGB because skin pixels are always
    red-dominant in BGR regardless of actual undertone, making RGB
    useless for warm/cool discrimination.
    """
    x, y, w, h = face

    # Zone 1: forehead — upper 25% of face, centre 50% width
    forehead = image[
        y + int(h * 0.05) : y + int(h * 0.22),
        x + int(w * 0.25) : x + int(w * 0.75)
    ]

    # Zone 2: left cheek — middle height, left third
    left_cheek = image[
        y + int(h * 0.45) : y + int(h * 0.70),
        x + int(w * 0.10) : x + int(w * 0.35)
    ]

    # Zone 3: right cheek — mirror of left
    right_cheek = image[
        y + int(h * 0.45) : y + int(h * 0.70),
        x + int(w * 0.65) : x + int(w * 0.90)
    ]

    scores = []

    for zone in [forehead, left_cheek, right_cheek]:
        if zone.size == 0:
            continue

        mask = _skin_mask(zone)
        avg_lab = _avg_lab_masked(zone, mask)

        a_ch = float(avg_lab[1]) - 128.0
        b_ch = float(avg_lab[2]) - 128.0
        scores.append(b_ch - a_ch)

    if not scores:
        return "Neutral"

    warmth_score = np.mean(scores)

    if warmth_score > 5:
        return "Warm"
    elif warmth_score < -5:
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

    mask = _skin_mask(face_roi)
    lab = cv2.cvtColor(face_roi, cv2.COLOR_BGR2LAB)
    skin_pixels = lab[mask > 0]

    if len(skin_pixels) < 30:
        skin_pixels = lab.reshape(-1, 3)

    # Lightness (L channel, 0-255 in OpenCV LAB)
    brightness = np.mean(skin_pixels[:, 0])

    if brightness > 200:
        return "Very Fair"
    elif brightness > 175:
        return "Fair"
    elif brightness > 148:
        return "Medium"
    elif brightness > 120:
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