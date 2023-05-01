# TODO
from cs50 import get_int


while True:
    height = get_int("Height: ")
    if 0 < height <= 8:
        break


for i in range(height):
    for j in range(height):
        if (i + j < height - 1):
            print(" ", end="")
        else:
            print("#", end="")
    print()
