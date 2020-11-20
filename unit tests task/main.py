from SimpleNumbersGenerator import *


def main():
    while True:
        print("Start - 1")
        print("Quit - 0")

        option = int(input())

        if option == 1:
            sng = SimpleNumbersGenerator()
            print(sng.generate(10))
        elif option == 0:
            break


if __name__ == '__main__':
    main()
