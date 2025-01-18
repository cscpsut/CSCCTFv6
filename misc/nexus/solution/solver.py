import numpy as np  # pip install numpy
from PIL import Image  # pip install pillow
from base64 import b64encode, b64decode
from pwn import *  # pip install pwntools
from z3 import *  # pip install z3-solver
import pytesseract  # https://github.com/tesseract-ocr/tesseract/releases/tag/5.5.0
import cv2

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def solve(eqs: list) -> dict:
    """Solve the equations

    Args:
        eqs (list): List of equations

    Returns:
        dict: Solution
    """
    solver = Solver()
    a1, a2, a3, a4, a5, a6, a7, a8, a9 = Ints("a1 a2 a3 a4 a5 a6 a7 a8 a9")
    eq1, eq2, eq3, eq4, eq5, eq6 = eqs

    solver.add(eval(eq1.replace("==", "==")))
    solver.add(eval(eq2.replace("==", "==")))
    solver.add(eval(eq3.replace("==", "==")))
    solver.add(eval(eq4.replace("==", "==")))
    solver.add(eval(eq5.replace("==", "==")))
    solver.add(eval(eq6.replace("==", "==")))

    if solver.check() == sat:
        if "div0" in str(solver.model()):
            return 0
        return solver.model()
    else:
        return 0


def get_binary_image(img: Image) -> Image:
    """Convert image to binary

    Args:
        img (Image): pillow image

    Returns:
        Image: binary image
    """
    img = img.convert("L")
    img = img.point(lambda x: 0 if x < 255 else 255, "1")
    return img


def extract_nums(img: Image) -> list:
    """Extract aymbols from image

    Args:
        img (Image): original image

    Returns:
        list: list of symbols
    """

    img.show()
    im2 = get_binary_image(img)
    im2 = np.array(im2, dtype=np.uint8)
    kernel = np.ones((3, 3), np.uint8)
    im3 = cv2.dilate(im2, kernel, iterations=1)

    img = Image.fromarray(im3)
    width, height = img.size
    cell_height = height // 5
    cell_width = width // 5
    extracted = []
    for i in range(5):
        for j in range(5):
            x = j * cell_width
            y = i * cell_height
            box = (x, y, x + cell_width, y + cell_height)
            region = img.crop(box)
            region.save("region.png")
            image = cv2.imread("region.png", 0)
            thresh = cv2.threshold(
                image, 255, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
            )[1]

            if (i, j) in [(0, 3), (2, 3), (4, 3), (3, 0), (3, 2), (3, 4)]:
                data = "="
            elif i % 2 == 0 and j % 2 == 0:
                data = pytesseract.image_to_string(
                    thresh,
                    lang="eng",
                    config="--psm 6 -c tessedit_char_whitelist=0123456789",
                ).strip()
            else:
                data = pytesseract.image_to_string(
                    thresh,
                    lang="eng",
                    config="--psm 6 -c tessedit_char_whitelist==+-*x/",
                ).strip()

            extracted.append(data)

    for i in range(len(extracted)):
        extracted[i] = extracted[i].replace("=", "==")

    # we need to make sure that our programe got the - sign
    # we can also see that there is a pattern number, operator, number, operator, number.....
    for i in range(1, len(extracted), 2):
        extracted[i] = "-" if extracted[i] == "" else extracted[i]

    return extracted


def assemble_eqs(nums: list) -> list:
    """takes the extracted numbers and assembles the equations

    Args:
        nums (list): list of symbols

    Returns:
        list: list of equations
    """
    eqs = []
    nums = [nums[i : i + 5] for i in range(0, len(nums), 5)]

    alphas = iter(["a1", "a2", "a3", "a4", "a5", "a6", "a7", "a8", "a9"])
    rows = [nums[0], nums[2], nums[4]]
    for row in rows:
        eq = ""
        for num in row:
            eq += num if num != "" else next(alphas)
            if num.isnumeric():
                next(alphas)
            eq += " "
        eqs.append(eq)

    alphas = iter(["a1", "a4", "a7", "a2", "a5", "a8", "a3", "a6", "a9"])
    cols = [0, 2, 4]
    for col in cols:
        eq = ""
        for row in range(5):
            eq += nums[row][col] if nums[row][col] != "" else next(alphas)
            if nums[row][col].isnumeric():
                next(alphas)
            eq += " "
        eqs.append(eq)
    return eqs


def main():

    r = remote("95.111.237.101", 1337)
    print("-------- Starting solver --------")
    welcome = r.recvuntil(b"start\n")
    print(welcome.decode())
    r.sendline(b"a")
    while True:

        b64 = r.recvline().strip()
        img_arr = b64decode(b64)
        np_arr = np.array(eval(img_arr.decode()), dtype=np.uint8)

        img = Image.fromarray(np_arr)
        # img.show()

        print("[+] Image received")
        nums = extract_nums(img)
        print("[+] Extracted numbers")

        print(nums)

        eqs = assemble_eqs(nums)
        print("[+] Assembled equations")
        print(eqs)

        s = solve(eqs)
        values = [s[decl].as_long() for decl in s.decls()]
        sol = sum(values)
        print("[+] Solved equations")
        print(values)
        print(f"sum: {sol}")

        print("[*] Sending solution")
        r.recvline()
        r.sendline(str(sol).encode())

        responce = r.recvline()
        print(responce)
        if b"again" not in responce:

            break
    flag = r.recvall().decode()
    print(flag)


if __name__ == "__main__":
    main()
