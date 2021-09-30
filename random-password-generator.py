import sys
import random
import string
import argparse

parser = argparse.ArgumentParser(description="Process arguments")
parser.add_argument('--length', dest='length', help='Set the length of the password')
args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

length = int(args.length)

lower = string.ascii_lowercase
upper = string.ascii_uppercase
numbers = string.digits
symbols = string.punctuation

all = lower + upper + numbers + symbols
temp = random.sample(all, length)

password = "".join(temp)
print(password)
