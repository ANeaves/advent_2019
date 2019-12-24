import sys
import logging


if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    file_name = sys.argv[1]  # puzzle input

    image_width = 25
    image height = 6
    