import logging
import sys
from collections import defaultdict
from math import ceil

class Element(object):

    def __init__(self, element_name, min_prod, recipe):
        self.min_prod = int(min_prod)
        self.element = element_name
        self.recipe = []
        for amount, element in recipe:
            self.recipe.append((int(amount) / self.min_prod, element))

    def __repr__(self):

        return "<Element {}, made from: {}. Min Prod {}>".format(self.element, self.recipe, self.min_prod)


class NanoFactory(object):

    def __init__(self, file_name):
        self.elements = {}
        with open(file_name) as f:
            for line in f:
                line = line.strip()
                logging.debug(line)
                all_source, production = line.split("=>")
                min_prod, prod_element = production.strip().split(' ')
                recipe = []
                for source in all_source.strip().split(','):
                    amount, element = source.strip().split(' ')
                    recipe.append((amount, element))
                self.elements[prod_element] = Element(prod_element, min_prod, recipe)

    def get_base_ingredients(self, target, amount):
        needed_elements = defaultdict(int, {target: amount})
        ingredients = [self.elements[target]]

        while ingredients:  # while list of ingredients still contains items
            logging.debug("Current List of Ingredients: %s", ingredients)
            logging.debug("Required List: %s", needed_elements)
            ingredient = ingredients.pop()
            recipe = ingredient.recipe
            required_amount = needed_elements[ingredient.element]
            if required_amount % ingredient.min_prod != 0:
                required_amount = required_amount + ingredient.min_prod - required_amount % ingredient.min_prod
            for part in recipe:
                amount = part[0] * required_amount
                element = part[1]
                needed_elements[element] += amount  # add this amount of this element to the needed elements
                if element in self.elements:  # if its not in self.elements, it must be ORE. Or a bug
                    ingredients.append(self.elements[element])

            needed_elements[ingredient.element] -= required_amount
        return needed_elements
            




if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    file_name = sys.argv[1]
    factory = NanoFactory(file_name)

    logging.debug(factory.elements)
    needed_elements = factory.get_base_ingredients("FUEL", 1)
    logging.debug(needed_elements)
    logging.info("Required Ore for 1 Fuel: %d", needed_elements["ORE"])

