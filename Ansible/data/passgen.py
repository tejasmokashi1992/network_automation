#!/opt/python/bin/python3

import random

class password_gen:
    """Random Password genration class."""

    def passgen(self,arg):
        USER_STRINGS=[]
        username=arg.split(".")[0]
        MAX_LEN = 12

        DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        LOCASE_CHARACTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                     'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q',
                     'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
                     'z']

        UPCASE_CHARACTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                     'I', 'J', 'K', 'M', 'N', 'O', 'p', 'Q',
                     'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                     'Z']

        SYMBOLS = ['@', '#', '&']
        for i in username:
            USER_STRINGS.append(i)

        COMBINED_LIST = DIGITS + UPCASE_CHARACTERS + LOCASE_CHARACTERS + SYMBOLS + USER_STRINGS

        rand_digit = random.choice(DIGITS)
        rand_upper = random.choice(UPCASE_CHARACTERS)
        rand_lower = random.choice(LOCASE_CHARACTERS)
        rand_symbol = random.choice(SYMBOLS)
        rand_user_strings = random.choice(USER_STRINGS)

        temp_pass = rand_digit + rand_user_strings + rand_upper + rand_user_strings + rand_lower + rand_symbol + rand_user_strings

        for x in range(MAX_LEN - 7):
            temp_pass = temp_pass + random.choice(COMBINED_LIST)

        return(temp_pass)
