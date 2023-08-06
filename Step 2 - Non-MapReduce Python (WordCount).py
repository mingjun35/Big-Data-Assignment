#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 19:35:54 2023

@author: leemingjun
"""


from collections import defaultdict
import re
import time

def mapper(dataframe, column_name):
    # Initialize an empty list to collect the mapped results
    mapped_data = []
    
    # Record the start time of the mapper function
    mapper_start_time = time.time()
    
    # Iterate through the specified column of the DataFrame and apply the mapping logic
    for line in dataframe[column_name]:
        
        if isinstance(line, str):
            line = line.strip() #remove leading and trailing whitespaces from each line
            words = line.split() #split the line into words
            for word in words:
                # Filter logic to exclude words containing both alphabetic and numeric characters
                if not (re.search(r'[a-zA-Z]', word) and re.search(r'\d', word) or re.search(r'\W', word)):
                    mapped_data.append((word, 1)) #append into the list
        
        elif isinstance(line, float):  # Check if the value is a float
            # Convert the float value to a string and apply the same string operations
            line_str = str(line)
            words = line_str.strip().split()
            for word in words:
                # Filter logic to exclude words containing both alphabetic and numeric characters
                if not (re.search(r'[a-zA-Z]', word) and re.search(r'\d', word) or re.search(r'\W', word)):
                    mapped_data.append((word, 1))  # Append into the list
            
    # Record the end time of the mapper function
    mapper_end_time = time.time()

    # Calculate the processing time of the mapper function in seconds
    mapper_processing_time = mapper_end_time - mapper_start_time
    
    return mapped_data, mapper_processing_time



def reducer(data):
    word_counts = defaultdict(int)
    
    # Record the start time of the reducer function
    reducer_start_time = time.time()
    
    #Iterates through each word-count pair in the input data
    for word, count in data: 
        try:
            count = int(count) #convert count into integer
        except ValueError:
            continue
        
        # Filter logic to exclude words containing both numeric and character characters
        #if not (re.search(r'[a-zA-Z]', word) and re.search(r'\d', word)):
            #continue
        
        word_counts[word] += count
        
    #Creates a new list called result by converting the word_counts defaultdict into a list of tuples. 
    #Each tuple contains a word and its corresponding count, representing the final reduced word-count pairs.
    result = [(word, count) for word, count in word_counts.items()]
    
    # Record the end time of the reducer function
    reducer_end_time = time.time()

    # Calculate the processing time of the reducer function in seconds
    reducer_processing_time = reducer_end_time - reducer_start_time
    
    return result, reducer_processing_time
    


mapped_data, mapper_processing_time = mapper(data, 'review/text')
print(mapper_processing_time)
print(mapped_data[:5])

result_list, reducer_processing_time = reducer(mapped_data)
print(reducer_processing_time)
print(result_list[:5])


######## Calculate Total Processing Time ########

total_processing_time = mapper_processing_time + reducer_processing_time

formatted_total_processing_time = "{:.2f}s".format(total_processing_time)

print(formatted_total_processing_time)



# has_duplicates = len(result_list) != len(set(word for word, _ in result_list))
# print("Has duplicates:", has_duplicates)