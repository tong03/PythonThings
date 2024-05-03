import hashlib
import time
import string
import itertools
import multiprocessing

# Load in passwords from file
file = open('hashes.txt', 'r')
read = file.readlines()
hashes = []

for line in read:
    if line not in hashes:
        hashes.append(line.strip())

characters = string.ascii_lowercase + string.ascii_uppercase + string.digits + "!@#$%^&*()"

for hash in hashes:
    print("Hash:", hash)
    found = False
    start = time.time()
    minutes = 0
    len = 1

    for length in range(1,10):
        if length > len:
            print("Length:", length)
            len  = length
        if found:
            break
        for combination in itertools.product(characters, repeat=length):
            guess = ''.join(combination)
            encoded = guess.encode('utf-8')
            md5_hash = hashlib.md5(encoded.strip()).hexdigest()

            if md5_hash == hash:
                end = time.time()
                print("Password:", guess)
                print("Time Elapsed:", end-start, 'seconds\n')
                found = True
                break

            current = time.time()
            curr_min = int((current - start) // 60)

            if curr_min > minutes:
                print(curr_min, "minute(s) have passed.")
                minutes = curr_min
