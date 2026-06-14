def get_style_personality(
    undertone,
    skin_tone
):

    if undertone == "Warm":

        if skin_tone in [
            "Dark",
            "Brown",
            "Very Dark"
        ]:

            return {
                "title":
                "Warm Earthy Classic",

                "description":
                "Rich earthy colors and traditional Indian tones complement your natural warmth."
            }

        else:

            return {
                "title":
                "Golden Spring",

                "description":
                "Warm bright shades and elegant gold accents suit your complexion beautifully."
            }

    elif undertone == "Cool":

        return {
            "title":
            "Elegant Winter",

            "description":
            "Jewel tones and cool sophisticated colors enhance your appearance."
        }

    else:

        return {
            "title":
            "Modern Neutral",

            "description":
            "Balanced colors and versatile styling choices work best for you."
        }