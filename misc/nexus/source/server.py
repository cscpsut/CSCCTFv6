from geneq import find_eqs
from genimage import get_image
from PIL import Image
from icecream import ic
from base64 import b64encode, b64decode
import os
import time

# the player must return the sum of missing values


def main():
    print("I heard you like math :)\npress any key to start")
    input()

    ans_count = 0
    done = False
    while True:
        eq, sol = find_eqs(1)

        correct_ans = 0
        sol = str(sol).replace("]", "").split(",")

        for i in sol:
            i = i.split(" ")
            correct_ans += int(i[-1])

        arr = get_image(eq)
        img = Image.fromarray(arr)
        # img.show()

        b64 = b64encode(str(arr.tolist()).encode()).decode()
        print(b64)
        start_t = time.time()

        print("Enter thea sum of missing values: ")
        answer = input()
        end_t = time.time()

        if end_t - start_t > 10:
            print("You took too long!")
            break

        if not answer.replace("-", "").isnumeric():
            print("idk if you know but math is all about numbers")
            break
        elif int(answer) == correct_ans:
            ans_count += 1
            if ans_count == 5:
                done = True
                break
            print("again!")
        else:
            print("This might help: https://study.com/academy/course/algebra.html")
            break

    if done:
        print("You are a math genius!")
        print("Here is your flag: ")
        flag = os.environ["FLAG"]
        print(flag)
        # print("CSCCTF{arcane_is_peak}")


if __name__ == "__main__":
    main()
