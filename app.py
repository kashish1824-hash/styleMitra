from flask import Flask, render_template, request
import os
import cv2

from utils.face_analysis import (
    detect_face,
    get_undertone,
    get_skin_tone,
    get_hair_color
)

from utils.stylist_model import (
    get_recommendation
)

from utils.indian_style import (
    get_indian_style
)

from utils.stylePersonality import (
    get_style_personality
)

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():

    return render_template(
        "index.html"
    )


@app.route(
    "/analyze",
    methods=["POST"]
)
def analyze():

    image = request.files["image"]

    image_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        image.filename
    )

    image.save(
        image_path
    )

    image_cv, faces = detect_face(
        image_path
    )

    largest_face = None
    largest_area = 0

    for (x, y, w, h) in faces:

        area = w * h

        if area > largest_area:

            largest_area = area

            largest_face = (
                x,
                y,
                w,
                h
            )

    face_count = 0

    undertone = "Neutral"
    skin_tone = "Medium"
    hair_color = "Black"

    if largest_face:

        x, y, w, h = largest_face

        cv2.rectangle(
            image_cv,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            3
        )

        face_count = 1

        undertone = get_undertone(
            image_cv,
            largest_face
        )

        skin_tone = get_skin_tone(
            image_cv,
            largest_face
        )

        hair_color = get_hair_color(
            image_cv,
            largest_face
        )

    detected_path = (
        "static/uploads/detected.jpg"
    )

    cv2.imwrite(
        detected_path,
        image_cv
    )

    height = request.form[
        "height"
    ]

    body_proportion = request.form[
        "body_proportion"
    ]

    torso_length = request.form[
        "torso_length"
    ]

    recommendation = get_recommendation(
        undertone=undertone,
        body_proportion=body_proportion,
        torso_length=torso_length
    )

    indian_style = get_indian_style(
        undertone,
        body_proportion
    )

    style_personality = get_style_personality(
        undertone,
        skin_tone
    )

    print("\nHair Color:", hair_color)
    print("Skin Tone:", skin_tone)
    print("Undertone:", undertone)

    return render_template(

        "result.html",

        image_path=detected_path,

        face_count=face_count,

        height=height,

        body_proportion=body_proportion,

        torso_length=torso_length,

        undertone=undertone,

        skin_tone=skin_tone,

        hair_color=hair_color,

        recommendation=recommendation,

        indian_style=indian_style,

        style_personality=style_personality

    )


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=os.environ.get("FLASK_DEBUG") == "1"
    )
