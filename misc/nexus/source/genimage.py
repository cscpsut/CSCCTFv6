from PIL import Image, ImageDraw, ImageFont
from geneq import find_eqs
import numpy as np


def get_image(eq: list = []) -> np.ndarray:
    rows = eq[:3]
    cols = eq[3:]

    # Colors for the grid
    circle_colors = [
        ["black", "orange", "black", "orange", "black"],
        ["orange", "None", "orange", "None", "orange"],
        ["black", "orange", "black", "orange", "black"],
        ["orange", "None", "orange", "None", "orange"],
        ["black", "orange", "black", "orange", "black"],
    ]

    # Image size and circle parameters
    cell_size = 100
    circle_radius = 40
    image_size = 5 * cell_size, 5 * cell_size

    # Create a new image with a black background
    image = Image.new("RGB", image_size, "gray")
    draw = ImageDraw.Draw(image)

    # Load a font

    font = ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size=40
    )

    # Draw the grid
    for row in range(5):
        for col in range(5):
            if circle_colors[row][col] == "None":
                continue
            color = circle_colors[row][col]
            text = eq[row][col]

            # Circle position
            x0 = col * cell_size + (cell_size - 2 * circle_radius) // 2
            y0 = row * cell_size + (cell_size - 2 * circle_radius) // 2
            x1 = x0 + 2 * circle_radius
            y1 = y0 + 2 * circle_radius

            # Draw circle
            draw.ellipse([x0, y0, x1, y1], fill=color)

    target_rows = [0, 2, 4]
    for r in range(len(rows)):
        tmp = rows[r].split(" ")
        for c in range(len(tmp)):
            text = tmp[c].replace("==", "=")

            text = (
                ""
                if text in ["a1", "a2", "a3", "a4", "a5", "a6", "a7", "a8", "a9"]
                else text
            )
            if text:
                text_width, text_height = font.getbbox(text)[
                    2:
                ]  # Using getbbox to calculate text size
                text_x = c * cell_size + (cell_size - text_width) // 2
                text_y = target_rows[r] * cell_size + (cell_size - text_height) // 2
                text_color = "white"
                draw.text((text_x, text_y), text, fill=text_color, font=font)

    target_cols = [0, 2, 4]
    for c in range(len(cols)):
        tmp = cols[c].split(" ")
        for r in range(len(tmp)):
            text = tmp[r].replace("==", "=")

            text = (
                ""
                if text in ["a1", "a2", "a3", "a4", "a5", "a6", "a7", "a8", "a9"]
                else text
            )
            if text:
                text_width, text_height = font.getbbox(text)[
                    2:
                ]  # Using getbbox to calculate text size
                text_x = target_cols[c] * cell_size + (cell_size - text_width) // 2
                text_y = r * cell_size + (cell_size - text_height) // 2
                text_color = "white"
                draw.text((text_x, text_y), text, fill=text_color, font=font)

    # image.show()

    arr = np.array(image)
    return arr


if __name__ == "__main__":
    get_image()
