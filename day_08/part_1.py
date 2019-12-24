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

    layer_vals = {}
    for index, layer in enumerate(layers):
        layer_0 = 0
        layer_1 = 0
        layer_2 = 0
        for line in layer:
            layer_0 += line.count('0')
            layer_1 += line.count('1')
            layer_2 += line.count('2')
        layer_vals[layer_0] = {
            "index": index,
            "1": layer_1,
            "2": layer_2
        }
    logging.debug(layer_vals)

    # find lowest 0 value
    value = layer_vals[min(layer_vals.keys())]["1"] * layer_vals[min(layer_vals.keys())]["2"]
    logging.info("Layer Val: %d", value)