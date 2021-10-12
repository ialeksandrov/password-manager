import sys
import random
import string
import argparse

generated_passwords = 'generated_passwords.txt'
saved_passwords = 'saved_passwords.txt'


def generate_password(length):
    length = int(args.length)
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    numbers = string.digits
    symbols = string.punctuation
    full_set = lower + upper + numbers + symbols
    temp = random.sample(full_set, length)
    password = "".join(temp)
    with open(generated_passwords, 'a+') as f:
        f.write(', '.join(f.read().split('\n')) + password + '\n')

    return password


def save_password():
    with open(generated_passwords, 'r') as file:
        with open(saved_passwords, 'a') as f:
            lines = file.readlines()[-1]
            f.write(lines)

    return lines


def list_saved_password():
    with open(saved_passwords, 'r') as fp:
        lines = fp.readlines()

    return lines


parser = argparse.ArgumentParser(description="Password management tool")
parser.add_argument('--length', dest='length', help='Set the length of the password')
parser.add_argument('--save', dest='save', help='Save the password')
subparser = parser.add_subparsers()
save_parser = subparser.add_parser('save_password', help='Save the generated password.')
list_parser = subparser.add_parser('list', help='List all saved passwords.')
save_parser.set_defaults(func=save_password)
list_parser.set_defaults(func=list_saved_password)
args = parser.parse_args()


if sys.argv[1] == '--length':
    print(generate_password(args.length))

if sys.argv[-1] == 'save_password':
    print(save_password())

if sys.argv[-1] == 'list':
    print(list_saved_password())