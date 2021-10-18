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
    converted_list = []
    with open(saved_passwords, 'r') as fp:
        lines = fp.readlines()
        for line in lines:
            converted_list.append(line.strip())

    return converted_list


def list_saved():
    last_saved = []
    with open(saved_passwords, 'r') as fp:
        lines = fp.readlines()[-1]
        last_saved.append(lines.strip())

    return last_saved


# FIXME: read the file, then convert the output to a list and then remove the specified element.
def remove_password(password):
    result = []
    with open(saved_passwords, 'r') as file:
        for lines in file:
            if args.password in lines:
                lines = lines.replace(args.password, '')
        result.append(lines.strip())

    with open(saved_passwords, 'w+') as f:
        for lines in result:
            f.write(lines.strip())

    return result


parser = argparse.ArgumentParser(description="Password management tool")
parser.add_argument('--length', dest='length', help='Set the length of the password')
parser.add_argument('--remove', dest='password', help='Remove old or unused passwords')
sub_parser = parser.add_subparsers()
save_parser = sub_parser.add_parser('save_password', help='Save the generated password.')
list_parser = sub_parser.add_parser('list', help='List all saved passwords.')
list_last_parser = sub_parser.add_parser('list_saved', help='Show the last saved password.')
save_parser.set_defaults(func=save_password)
list_parser.set_defaults(func=list_saved_password)
list_last_parser.set_defaults(func=list_saved)
if len(sys.argv) == 1:
    parser.print_help(sys.stderr)
    sys.exit(1)
args = parser.parse_args()


if sys.argv[1] == '--length':
    print(generate_password(args.length))

if sys.argv[-1] == 'save_password':
    print(save_password())

if sys.argv[-1] == 'list':
    print(list_saved_password())

if sys.argv[-1] == 'list_saved':
    print(list_saved())

if sys.argv[1] == '--remove':
    print(remove_password(args.password))
