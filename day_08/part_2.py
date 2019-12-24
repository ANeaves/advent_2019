import sys
import logging


if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    file_name = sys.argv[1]  # puzzle input

    image_height = 6
    image_width = 25

    layers = []
    layers.append([])
    file_string = ''
    with open(file_name) as f:
        file_string = f.read()

    logging.debug(file_string)

    layer_num = 0
    line_num = -1
    for index, char in enumerate(file_string):
        # char = int(char)
        if index % image_width == 0:
            line_num += 1
            layers[layer_num].append('')
            # logging.debug("New Line num: %d", line_num)
        if line_num % image_height == 0 and line_num != 0:
            layers[-1].pop(-1)
            layer_num += 1
            line_num = 0
            layers.append([''])
            # logging.debug("New Layer num: %d", layer_num)
            # logging.debug(layers)
        # logging.debug("Appending (%s) to [%d][%d]", char, layer_num, line_num)
        layers[-1][-1] += char
        # logging.debug(layers)
    logging.debug(layers)


    final_image = {}

    for layer in layers:
        # for each char, if its not 2, add it to the final image
        for y, line in enumerate(layer):
            for x, char in enumerate(line):

                if not final_image.get((x, y)) and char != '2':
                    if char == '1':
                        # then its a white pixel
                        final_image[(x, y)] = '#'
                    else:
                        # black pixel
                        final_image[(x, y)] = ' '


logging.info(final_image)

for y in range(image_height):
    line = ''
    for x in range(image_width):
        line += final_image[(x, y)]
    logging.info(line)