#!/usr/bin/python3

import sys
import tempfile
import os
import hashlib
import string
import random 

def validate_url(url):
    if 'http://' in url or 'https"//' in url:
        return True
    return False

def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

def powx():
    rnd = randomword(32).encode()
    hsh = hashlib.sha256(rnd)
    sys.stdout.write("Try to break my pow: "+hsh.hexdigest()[-6:])
    sys.stdout.write(">>");
    sys.stdout.flush()
    data = sys.stdin.readline().encode()[:-1]
    sys.stdout.write("Your data: "+data.decode('Utf-8'))
    user_hsh = hashlib.sha256(data)
    sys.stdout.write("Sha256 from your data: "+user_hsh.hexdigest()[-6:])
    if user_hsh.hexdigest()[-6:] == hsh.hexdigest()[-6:]:
        return True
    else:
        return False

def main():
    if not powx():
        print("Invalid pow")
        return
    sys.stdout.write("Enter your Url:")
    sys.stdout.write(">>");
    sys.stdout.flush()

    url = sys.stdin.readline();
    if validate_url(url):
        os.system("./chrome/chrome --headless=new --disable-gpu --enable-blink-features=MojoJS " + url)
    else:
        print('Invalid url')


if __name__ == "__main__":
    main()


