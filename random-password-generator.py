import sys
import random
import string
import argparse


generated_passwords = 'generated_passwords.txt'


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
        saved_passwords = []
        lines = file.readlines()[-1]
        saved_passwords.append(lines.strip())
        print(saved_passwords)

        return saved_passwords


parser = argparse.ArgumentParser(description="Password management tool")
parser.add_argument('--length', dest='length', required=True, help='Set the length of the password')
parser.add_argument('--save', dest='save', help='Save the password')
subparser = parser.add_subparsers()
save_parser = subparser.add_parser('save_password', help='Save the generated password.')
save_parser.set_defaults(func=save_password)
args = parser.parse_args()


print(generate_password(12))
print(save_password())

