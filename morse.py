#!/usr/bin/env python3

import argparse
import sys

morse = {'a':'.-', 'b':'-...', 'c':'-.-.', 'd':'-..', 'e':'.',
         'f':'..-.', 'g':'--.', 'h':'....', 'i':'..', 'j':'.---',
         'k':'-.-', 'l':'.-..', 'm':'--', 'n':'-.', 'o':'---',
         'p':'.--.', 'q':'--.-', 'r':'.-.', 's':'...', 't':'-',
         'u':'..-', 'v':'...-', 'w':'.--', 'x':'-..-',
         'y':'-.--', 'z':'--..', ' ':''}

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--message", type=str, help="Message to be converted")
    parser.add_argument("-i", "--input", help="Input file")
    parser.add_argument("-o", "--output", help="Output file")
    parser.add_argument("-e","--encrypt", action='store_true', help="Encrypt message (force)")
    parser.add_argument("-d","--decrypt", action='store_true', help="Decrypt message (force)")
    parser.add_argument("-v","--verbose", type=int, choices=[0,1,2], default=0,
                   help="increase output verbosity (default: %(default)s)")

    return parser.parse_args()

def encrypt(message, args):
    result = []
    for char in message:
        if char in morse:
            print(morse[char])
            result.append(morse[char])
    result = remove_blanks(result)
    result = '/' + '/'.join(result) + '//'

    return result

def decrypt(message, args):
    pass

def remove_blanks(lst):
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
    if args.message:
        message = args.message.lower()
    else:
        try:
            message = open(args.input, 'r').read()
        except IOError:
            print("Could not find message or open file '%s'" % args.input)
            sys.exit(1)

    if any(char.isalpha() for char in message) or args.encrypt:
        action = 'encrypt'
    else:
        action = 'decrypt'
    if args.decrypt:
        action = 'decrypt'

    if action == 'encrypt':
        encrypt(message, args)
    else:
        decrypt(message, args)

if __name__ == '__main__':

    if sys.version_info < (3, 5, 0):
        sys.stderr.write("You need python 3.5 or later to run this script\n")
        sys.exit(1)

    try:
        arguments = parse_args()
    except SystemExit:
        print('Try $python morse.py "Hello" 123 --enable')
        sys.exit(1)

    main(arguments)
