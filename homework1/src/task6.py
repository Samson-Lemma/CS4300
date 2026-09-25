def count_words(filename):
    with open(filename, "r", encoding="utf-8") as file:
        contents = file.read()

    return len(contents.split())


if __name__ == "__main__":
    print(count_words("task6_read_me.txt"))