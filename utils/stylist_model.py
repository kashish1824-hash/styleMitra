# Rule-based recommendation engine.
#
# These mappings were derived through EDA of stylist_dataset.csv:
# each output field was found to be fully determined by a single
# input field (Under Tone, Body Proportion, or Torso Length), so a
# direct lookup table is more accurate and transparent than a
# clustering model trained on the same data.

UNDERTONE_MAP = {
    "Warm": {
        "Recommended Clothing Colors":
            "Earth Tones, Olive, Coral, Peach, Mustard, Warm Red",
        "Avoid Clothing Colors":
            "Cool Blue, Icy Gray, Jewel Tones",
        "Recommended Jewelry Metal":
            "Gold",
        "Recommended Clothing Color Wheel Region":
            "Warm colors (red, orange, yellow, warm greens)",
    },
    "Cool": {
        "Recommended Clothing Colors":
            "Jewel Tones, Icy Blue, Lavender, Silver, Emerald",
        "Avoid Clothing Colors":
            "Orange, Mustard, Brown",
        "Recommended Jewelry Metal":
            "Silver",
        "Recommended Clothing Color Wheel Region":
            "Cool colors (blue, green, violet, cool grays)",
    },
    "Neutral": {
        "Recommended Clothing Colors":
            "Soft Pinks, Plums, Teal, Neutral Beige",
        "Avoid Clothing Colors":
            "Fluorescents, Harsh Yellow",
        "Recommended Jewelry Metal":
            "Rose Gold",
        "Recommended Clothing Color Wheel Region":
            "Neutral-friendly zones (balanced warm/cool like teal, plum, taupe)",
    },
}

BODY_PROPORTION_MAP = {
    "Apple": {
        "Recommended Fitting Style": "Empire Waist",
        "Recommended Patterns": "Dark Solid Tops",
    },
    "Hourglass": {
        "Recommended Fitting Style": "Tailored Fit",
        "Recommended Patterns": "Subtle Prints",
    },
    "Inverted Triangle": {
        "Recommended Fitting Style": "A-Line Bottoms",
        "Recommended Patterns": "Vertical Stripes",
    },
    "Oval": {
        "Recommended Fitting Style": "Wraps and Empire",
        "Recommended Patterns": "Diagonal Lines",
    },
    "Rectangle": {
        "Recommended Fitting Style": "Defined Waist",
        "Recommended Patterns": "Curved Lines",
    },
    "Trapezoid": {
        "Recommended Fitting Style": "Balanced Fit",
        "Recommended Patterns": "Simple Solids",
    },
    "Triangle": {
        "Recommended Fitting Style": "Emphasize Top",
        "Recommended Patterns": "Bright Tops",
    },
}

TORSO_LENGTH_MAP = {
    "Short Torso": {
        "Recommended Shoes": "Low Heels or Flats",
    },
    "Long Torso": {
        "Recommended Shoes": "Heels or Platforms",
    },
    "Balanced": {
        "Recommended Shoes": "Any Style",
    },
}


def get_recommendation(undertone, body_proportion, torso_length):
    """
    Build a recommendation by looking up each output field from the
    input dimension that determines it.

    undertone: "Warm" | "Cool" | "Neutral"
    body_proportion: one of BODY_PROPORTION_MAP keys
    torso_length: one of TORSO_LENGTH_MAP keys
    """

    undertone_data = UNDERTONE_MAP.get(undertone, UNDERTONE_MAP["Neutral"])

    body_data = BODY_PROPORTION_MAP.get(
        body_proportion,
        BODY_PROPORTION_MAP["Rectangle"]
    )

    torso_data = TORSO_LENGTH_MAP.get(
        torso_length,
        TORSO_LENGTH_MAP["Balanced"]
    )

    recommendation = {}
    recommendation.update(undertone_data)
    recommendation.update(body_data)
    recommendation.update(torso_data)

    return recommendation
