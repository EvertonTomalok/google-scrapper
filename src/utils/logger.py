from os import getenv
from pprint import pprint

try:
    DEBUGGING = getenv("DEBUG", "False")
except Exception as err:
    print("Debugging err: ", err)
    DEBUGGING = False


def print_logger(*args):
    if DEBUGGING:
        print(*args, end="\n\n-------\n\n")


def pprint_logger(msg):
    if DEBUGGING:
        pprint(msg)
        print("\n\n------------\n\n")
