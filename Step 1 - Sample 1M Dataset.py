#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 10:34:46 2023

@author: leemingjun
"""

import pandas as pd
import numpy as np

# Load your dataset into a pandas DataFrame
dataset = pd.read_csv('/Users/leemingjun/Documents/Semester 9 - April 2023/Big Data Analytics in Cloud/Datasets for Testing/Amazon Book Review/Books_rating.csv')

step = 3
sample_size = 1000000

def systematic_sampling(dataset, step, sample_size):
    total_rows = step * sample_size
    indexes = np.arange(0,total_rows,step=step)
    systematic_sample = dataset.iloc[indexes[:sample_size]]
    
    # Retain only 'book_title' and 'review/text' columns
    systematic_sample = systematic_sample[['review/text']]
    
    return systematic_sample


data = systematic_sampling(dataset, step, sample_size)


# # Export the systematic sample to a text file
#data.to_csv('/Users/leemingjun/Documents/Semester 9 - April 2023/Big Data Analytics in Cloud/Amazon Book Review 1M.txt', sep='\t', index=False)
