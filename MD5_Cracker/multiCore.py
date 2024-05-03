import hashlib
import time
import string
import itertools
import multiprocessing as mp

# Function to solve a range of combinations
def solve_combinations(hash, start, end, characters, length):
    # itertools.islice is used to split the work load into chunks -- fitting for multi-cores
    for combination in itertools.islice(itertools.product(characters, repeat=length), start, end):
        guess = ''.join(combination)
        encoded = guess.encode('utf-8')
        md5_hash = hashlib.md5(encoded).hexdigest()
        
        if md5_hash == hash:
            return guess  # Found the password
        
    return None  # Filler if password not found for given length

# Wrapper function for multiprocessing
def brute_force_hash(hash, characters):
    print("Hash:", hash)
    # intialize marker to exit early
    found = False
    start = time.time()

    # find number of processes to use
    num_processes = mp.cpu_count()
    
    # try varying password lengths, starting with 1
    for length in range(1, 10):
        print("Trying length:", length)
        
        # calculate the total number of combinations for the current length
        total_combinations = len(characters) ** length
        
        # divide the work among the cores (processes)
        chunk = total_combinations // num_processes
        ranges = [(i * chunk, (i + 1) * chunk) for i in range(num_processes)]
        
        # multiprocessing Pool to parallelize the task
        with mp.Pool(processes=num_processes) as pool:
            # apply_async divides function across multiple inputs
            results = [pool.apply_async(solve_combinations, args=(hash, start, end, characters, length)) for start, end in ranges]

            # Wait for the results
            for result in results:
                password = result.get()
                # check if password is True -- which cannot be None
                if password:
                    found = True
                    end = time.time()
                    print("Password:", password)
                    if(int((end - start) // 60) > 0):
                        print("Time Elapsed:", (end-start) // 60, 'minute(s)\n')
                    else:
                        print("Time Elapsed:", end - start, 'seconds\n')
                        break
        # end computation early if found flag is True
        if found:
            break

def main():
    # Load hashes
    with open('hashes.txt', 'r') as file:
        read = file.readlines()
        hashes = []
        for line in read:
            if line not in hashes:
                hashes.append(line.strip())

    # Initialize available characters
    characters = string.ascii_lowercase + string.ascii_uppercase + string.digits + "!@#$%^&*()"
    
    # Call brute_force function for each hash
    for hash in hashes:
        brute_force_hash(hash, characters)





if __name__ == '__main__':
    main()
