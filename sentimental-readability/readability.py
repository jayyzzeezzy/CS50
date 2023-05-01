# TODO
from cs50 import get_string


def main():

    # ask user to type text
    text = get_string("Text: ")

    # print user input
    for i in text:
        print(f"{text}")

    # use function to count letters
    letter = count_letters(text)
    print(f"{letter}")

    # use function to count words
    word = count_words(text)
    print(f"{word}")

    # use function to count sentences
    sentence = count_sentences(text)
    print(f"{sentence}")

    # use function to calculate grade level
    grade = cal_grade_level(letter, sentence, word)
    if grade >= 16:
        print("Grade 16+")
    elif grade < 1:
        print("Before Grade 1")
    else:
        print(f"Grade {grade}")


# define how count letters function work. sampled from my work in PS2
def count_letters(excerpt):
    letter = 0
    for i in excerpt:
        if i.isalpha():
            letter += 1
    return letter


# define how count words function work. sampled from my work in PS2
def count_words(excerpt):
    word = 1
    for i in excerpt:
        if i == " ":
            word += 1
    return word


# define how count sentences work
def count_sentences(excerpt):
    sentence = 0
    for i in excerpt:
        if i == "." or i == "?" or i == "!":
            sentence += 1
    return sentence


# define how calculate grade level work
def cal_grade_level(x, y, z):
    l = x / z * 100
    s = y / z * 100

    index = 0.0588 * l - 0.296 * s - 15.8
    return round(index)


if __name__ == "__main__":
    main()
