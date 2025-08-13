#!/usr/bin/env python3

import argparse
import sys

morse = {'a':'.-', 'b':'-...', 'c':'-.-.', 'd':'-..', 'e':'.',
         'f':'..-.', 'g':'--.', 'h':'....', 'i':'..', 'j':'.---',
         'k':'-.-', 'l':'.-..', 'm':'--', 'n':'-.', 'o':'---',
         'p':'.--.', 'q':'--.-', 'r':'.-.', 's':'...', 't':'-',
         'u':'..-', 'v':'...-', 'w':'.--', 'x':'-..-',
         'y':'-.--', 'z':'--..', ' ':'',
         '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
         '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----',
         '.': '.-.-.-', ',':'--..--', '?': '..--..', "'": '.----.', '!': '-.-.--',
         '/': '-..-.', '(': '-.--.', ')': '-.--.-', '&': '.-...', ':': '---...',
         ';': '-.-.-.', '=':'-...-', '+': '.-.-.', '-': '-....-', '_': '..--.-',
         '"': '.-..-.', '$': '...-..-', '@': '.--.-.'}

reverse_morse = {val: k for k, val in morse.items()}

DOTS = '.'
DASHES = '-'
DELIMITER = '/'

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--message", type=str, help="Message to be converted")
    parser.add_argument("-i", "--input", help="Input file")
    parser.add_argument("-o", "--output", help="Output file")
    parser.add_argument("-e","--encrypt", action='store_true', help="Encrypt message (force)")
    parser.add_argument("-d","--decrypt", action='store_true', help="Decrypt message (force)")
    parser.add_argument("-t","--dots", default='.', help="Dots character (default='.')")
    parser.add_argument("-c","--dashes", default='-', help="Dash character (default='-')")
    parser.add_argument("-l","--delimiter", default='/', help="Delimiter character (default='/')")
    parser.add_argument("-v","--verbose", type=int, choices=[0,1,2], default=0,
                   help="increase output verbosity (default: %(default)s)")

    return parser.parse_args()

def encrypt(message, args):
    global DOTS, DASHES, DELIMITER
    result = []
    for char in message:
        if char in morse:
            result.append(morse[char])
    result = remove_blanks(result)
    result = [item.replace('.', DOTS) for item in result]
    result = [item.replace('-', DASHES) for item in result]
    result = [item.replace('/', DELIMITER) for item in result]
    result = DELIMITER + DELIMITER.join(result) + 2 * DELIMITER

    return result

def decrypt(message, args):
    global DOTS, DASHES, DELIMITER
    result = []
    word = ''
    for char in message:
        if char == DOTS or char == DASHES:
            word = word + char
        if char == DELIMITER:
            result.append(word)
            word = ''
    result = remove_blanks(result)
    result = [item.replace(DOTS, '.') for item in result]
    result = [item.replace(DASHES, '-') for item in result]
    result = [item.replace(DELIMITER, '/') for item in result]

    result = [reverse_morse.get(code, '?') for code in result]
    result = ''.join(result)

    return result

def remove_blanks(lst):

    # Remove 2+ spaces or empty values to one
    result = []
    prev_blank = False
    for item in lst:
        if item == '':
            if not prev_blank:
                result.append(item)
            prev_blank = True
        else:
            result.append(item)
            prev_blank = False
    return result

def main(args):

    # Define message content (user input or file)
    if args.message:
        message = args.message.lower()
    else:
        try:
            message = open(args.input, 'r').read()
        except IOError:
            print("Could not find message or open file '%s'" % args.input)
            sys.exit(1)

    # Define action by message content or force argument
    if any(char.isalpha() for char in message) or args.encrypt:
        action = 'encrypt'
    else:
        action = 'decrypt'
    if args.decrypt:
        action = 'decrypt'

    # Set characters for processing
    global DOTS, DASHES, DELIMITER
    DOTS = args.dots
    DASHES = args.dashes
    DELIMITER = args.delimiter

    if action == 'encrypt':
        return encrypt(message, args)
    else:
        return decrypt(message, args)



if __name__ == '__main__':

    if sys.version_info < (3, 5, 0):
        sys.stderr.write("You need python 3.5 or later to run this script\n")
        sys.exit(1)

    try:
        arguments = parse_args()
    except SystemExit:
        print('Try $python morse.py "Hello" 123 --enable')
        sys.exit(1)

    print(main(arguments))
