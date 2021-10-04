import sys
import random
import string
import argparse

parser = argparse.ArgumentParser(description="Password management tool")
parser.add_argument('--length', dest='length', help='Set the length of the password')
parser.add_argument('--save', dest='save', help='Save the password')
args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

generated_passwords = 'generated_passwords.txt'


def generate_password(length):
    length = int(args.length)
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    numbers = string.digits
    symbols = string.punctuation
    all = lower + upper + numbers + symbols
    temp = random.sample(all, length)
    password = "".join(temp)
    with open(generated_passwords, 'a+') as f:
        f.write(', '.join(f.read().split('\n')) + password + '\n')

    return password


def save_password():
    with open(generated_passwords, 'r') as file:
        saved_passwords = []
        lines = file.readlines()[-1]
        saved_passwords.append(lines)

        return saved_passwords


#print(generate_password(12))
#print(save_password())
