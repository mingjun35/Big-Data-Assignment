#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 21:47:59 2023

@author: leemingjun
"""

#!/usr/bin/env python3
import sys
import time
import re

# Record the start time of the mapper job
mapper_start_time = time.time()

for line in sys.stdin:
    line = line.strip()
    words = line.split()
    for word in words:
        # Filter logic to exclude words containing both alphabetic and numeric characters
        # and any symbols (non-alphanumeric characters)
        if not (re.search(r'[a-zA-Z]', word) and re.search(r'\d', word) or re.search(r'\W', word)):
            print('%s\t%s' % (word, 1))

# Record the end time of the mapper job
mapper_end_time = time.time()

# Calculate the processing time of the mapper job in seconds
mapper_processing_time = mapper_end_time - mapper_start_time

# Output the mapper_processing_time to the standard output
print("Mapper Processing Time: %.2f" % mapper_processing_time)





#!/usr/bin/env python3
from operator import itemgetter
import sys
import time

# Record the start time of the reducer job
reducer_start_time = time.time()

current_word = None
current_count = 0
word = None

# Variable to store the mapper_processing_time from the input
mapper_processing_time = None

for line in sys.stdin:
    line = line.strip()

    # Check if the line contains the mapper_processing_time value
    if line.startswith("Mapper Processing Time: "):
        mapper_processing_time = float(line.split(": ")[1])
        continue

    word, count = line.split('\t', 1)

    try:
        count = int(count)
    except ValueError:
        continue

    if current_word == word:
        current_count += count
    else:
        if current_word:
            print('%s\t%s' % (current_word, current_count))
        current_count = count
        current_word = word

if current_word == word:
    print('%s\t%s' % (current_word, current_count))

# Calculate the total processing time by adding mapper_processing_time and reducer_processing_time
total_processing_time = mapper_processing_time + (time.time() - reducer_start_time)

# Output the total_processing_time to the console or log
print("Total Processing Time: %.2f seconds" % total_processing_time)