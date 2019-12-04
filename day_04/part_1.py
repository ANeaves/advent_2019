# pasword facts
# 6 digit number
# within range 307237-769058
# two ajacent digits are the same
# digits never decrease going left to right (ie 143 would be invalid because 4 > 3)

# maybe regex?
import re
import logging
def get_valid_passwords(pass_range):
    valid_words = []
    for word in pass_range:
        word = str(word)
        if has_double_digit(word) and never_decrease(word):
            valid_words.append(word)

    return valid_words

def has_double_digit(word):  # this is a cool method, micheal is smart
    word = str(word)
    char_list = [['']]
    for char in word:
        if char_list[-1][0] == char:
            char_list[-1].append(char)
        else:
            char_list.append([char])
    return any( len(digits) == 2 for digits in char_list)


def never_decrease(word):
    for i in range(len(word)-1):
        if int(word[i]) > int(word[i+1]):
            return False
    return True



if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    pass_range = range(307237, 769058) # range given by challenge
    valid_passwords = get_valid_passwords(pass_range)

    logging.debug(valid_passwords)
    logging.info("NUM VALID PASSWORDS: %d", len(valid_passwords))
