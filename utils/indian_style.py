# Hex codes for the named colors used in best_colors, so the UI
# can render accurate swatches.
COLOR_HEX = {
    "Mustard Yellow": "#D4A017",
    "Olive Green": "#556B2F",
    "Rust Orange": "#B7410E",
    "Maroon": "#800000",
    "Peach": "#F4A460",
    "Royal Blue": "#4169E1",
    "Lavender": "#B57EDC",
    "Emerald Green": "#046307",
    "Wine": "#722F37",
    "Silver Grey": "#C0C0C0",
    "Teal": "#008080",
    "Dusty Rose": "#C9A0A0",
    "Soft Navy": "#34495E",
    "Charcoal": "#36454F",
    "Taupe": "#8B7D6B",
}


# Fit guidance per Body Proportion, used to tailor the
# college/casual and office looks for Indian fashion contexts.
FIT_GUIDANCE = {
    "Apple": "Empire-line Kurta",
    "Hourglass": "Fitted Kurta with Belt",
    "Inverted Triangle": "A-Line Kurta",
    "Oval": "Flowy Anarkali Kurta",
    "Rectangle": "Straight-Cut Kurta",
    "Trapezoid": "Relaxed Straight Kurta",
    "Triangle": "Detailed Top with Plain Bottoms",
}


def get_indian_style(undertone, body_proportion):

    if undertone == "Warm":

        colors = [
            "Mustard Yellow",
            "Olive Green",
            "Rust Orange",
            "Maroon",
            "Peach"
        ]

        festive = [
            "Mustard Kurta",
            "Olive Nehru Jacket",
            "Maroon Silk Kurta"
        ]

    elif undertone == "Cool":

        colors = [
            "Royal Blue",
            "Lavender",
            "Emerald Green",
            "Wine",
            "Silver Grey"
        ]

        festive = [
            "Royal Blue Kurta",
            "Navy Bandhgala",
            "Wine Sherwani"
        ]

    else:

        colors = [
            "Teal",
            "Dusty Rose",
            "Soft Navy",
            "Charcoal",
            "Taupe"
        ]

        festive = [
            "Teal Kurta",
            "Grey Nehru Jacket",
            "Navy Indo-Western"
        ]

    fit = FIT_GUIDANCE.get(
        body_proportion,
        "Straight-Cut Kurta"
    )

    return {

        "best_colors": colors,

        "best_colors_hex": [
            COLOR_HEX.get(c, "#cccccc") for c in colors
        ],

        "festive": festive,

        "college_look":
            fit + " + Straight Fit Jeans + Sneakers",

        "office_look":
            fit + " + Tailored Trousers + Formal Shoes"

    }
