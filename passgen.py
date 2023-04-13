import string
import secrets


def pwgen():
    letters = string.ascii_letters
    digits = string.digits
    alphabet = letters + digits
    pwd = ''
    for i in range(7):
        pwd += ''.join(secrets.choice(alphabet))
    return pwd


with open('users.txt', 'r') as src, open('pwds.txt', 'w') as dst:
    for line in src:
        if len(line) > 3:
            dst.write(line.strip() + ':' + pwgen() + '\n')
