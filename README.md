## MD5 Password Cracker

This report is for the brute force hash cracking project written in Python. I created two script to compare the time between single-core and multi-core computing to evaluate their differences. Unfortunately, I was not able to crack all the passwords and only got to about 5 out of the 8 passwords before it started to take a large amount of time to crack. Regardless, these data are recorded below to show how much time it takes.

### Recorded Data:
<img width="468" alt="image" src="https://github.com/tong03/PythonThings/assets/111693394/75f392d1-3659-4b91-8421-79b6417b268f">


### Analysis:
Based on the data, I noticed that as the password length increases, the time it takes to crack them increases exponentially, as seen most prominently by the jump from password length 3 to password length 4 in both scenarios. I suspect that this might have to do with the exponential increase in total combinations that the script must do as the length increases. 

One surprising thing that I noticed was that for password length 3 or below, the single core was faster than the multi-core, and only at length 4 or higher did the multi-cores speed become superior. An explanation for this might be in how multiprocessing has higher overhead processes, which means it takes some time to start up and be recombined for each process. This cost is probably what makes the multi-core script run slower at length less than 3 since the total combinations is not large enough to justify the overhead time to setup multi-core. Once the total combinations are large enough (4+), then the strength of multiprocessing is shown.

### Improvements:
One clear way to increase the password cracking speed is the use of multi-cores computing. Since in Python, the default has Global Interpreter Lock (GIL), which only allow for one core to work at a time. This means that the computing speed is limited to how fast the 1 processor can generate each combination. By using the multiprocessing library, I was able to bypass this and unlock the use of multiple cores (8) for the script.

```
import multiprocessing as mp
with mp.Pool(processes=num_processes) as pool:
            results = [pool.apply_async(solve_combinations, args=(hash, start, end, characters, length)) for start, end in ranges]
```

Given the overhead time required for multiprocessing, a hybrid approach (single- and multi- core(s)) might help with optimizing the password time for all passwords. This can be done by using single-core computing for password length less than 4 and switching to multi-core computing for length 4 and above. For each password length, the total combinations are quickly calculated initially and then divided into even chunks and assigned to each processor. In this way, the computation for each chunk can occur concurrently instead of having to queue up, which helps improve the speed at which the passwords are cracked. In my data, with one core computing, I was able to crack the password of length 4 in 16 seconds and was not able to crack the password of length 5 in a reasonable time. In contrast, when using multi-cores, I was able to reduce the time for cracking the password of length 4 to only 4 seconds and was able to crack the password of length 5 in 443 seconds, which was previously impossible for the one core.

Additionally, this script used a brute force method to generate all possible password combinations. However, a more efficient approach will be using a dictionary attack, where an intuitive list of known words will be used as a starting point instead to test since a user is more likely to use a password derived from known words in the dictionary. By doing so, we significantly increase the cracking speed by bypassing the meaningless passwords that are unlikely to be used by real users. Similarly, a rainbow table is a data table containing hash value for all possible up to a certain length. While this takes time to create, once it is created it can be used to efficiently look up a hash value and find the actual password much quicker than the brute-force method. From online, I see that there are possible rainbow tables for MD5 hash and as such will be faster than a brute-force method if used.
