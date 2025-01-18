import numpy as np
from PIL import Image


def get_img(image, p=1, q=1):

    # Convert image to numpy array
    img_array = np.array(image)
    N = img_array.shape[0]

    # Create output array
    scrambled = img_array.copy()

    for i in range(69):
        # Apply Arnold's Cat Map
        temp = np.zeros_like(scrambled)
        for x in range(N):
            for y in range(N):
                x_new = (x + p * y) % N
                y_new = (q * x + (p * q + 1) * y) % N
                temp[x_new, y_new] = scrambled[x, y]
        scrambled = temp

    img = Image.fromarray(scrambled)
    return img


if __name__ == "__main__":
    image = Image.open("cat.png")
    img = get_img(image, 6, 8)
    img.show()
    img.save("scrambled_cat.png")
