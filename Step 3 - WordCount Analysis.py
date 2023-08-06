#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 15:23:15 2023

@author: leemingjun
"""

import pandas as pd

#Data Cleaning
import string
import re
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
import gensim
import gensim.corpora as corpora
import numpy as np

#Data Analysis
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from textblob import TextBlob



dataset=pd.read_csv('/Users/leemingjun/Documents/Semester 9 - April 2023/Big Data Analytics in Cloud/For Submission/part-00000-MJ.txt', sep='\t', header=None)

dataset.columns = ['key', 'value']


# Verify the data types
print(dataset.dtypes)

sorted_data = dataset.sort_values(by='value', ascending=False)


####################### Data Cleaning ##########################


####################### Tokenisation of Words ##########################


#Drop missing values in the dataset
data_final = dataset.dropna()


# Tokenisation of Amazon Books Reviews
data_final['tokens'] = data_final['key'].apply(word_tokenize).tolist()



####################### Cleaning the tokens ##########################

# Assign Stop Words
stop_words = stopwords.words('english')
stop_words.extend(['book', 'read', 'one', 'books', 'quot', 'also', 'would'])


# Stemming words to its root form, Ex. driving to driv. Because stemming does not consider the context of te word.
# Lemmatization is the process of grouping different inflected forms of word as a single item.
# Lemmatisation is a form of stemming but it considers the context of the word.
# For example, driving to drive
def lemmatize_sentence(tokens):
    lemmatizer = WordNetLemmatizer() # Assign variable to the function
    lemmatized_sentence = []
    for word, tag in pos_tag(tokens):
        if tag.startswith('NN'):
            pos = 'n' # tagging noun tokens with 'n' for lemmatizing process
            lemmatized_sentence.append(lemmatizer.lemmatize(word, pos))
    return lemmatized_sentence
    #print(word, tag, pos)

def remove_noise(review_tokens, stop_words):
    cleaned_tokens = []
    for token in review_tokens:
        token = re.sub('[0-9]','',token) # Remove numbers
        token = re.sub(r'[^\w.]', '', token) # Remove non-alphabet character like symbol and emoji
        if '.' in token:
            tokens_split = token.split('.') #Split 
            for split_token in tokens_split:
                split_token = split_token.replace("'", '')  # Remove single quote
                if len(split_token) > 0 and split_token not in string.punctuation and split_token.lower() not in stop_words:
                    cleaned_tokens.append(split_token.lower())
        else:
            token = token.replace("'", '')  # Remove single quote
            if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
                cleaned_tokens.append(token.lower())
    return cleaned_tokens





cleaned_tokens = []

# Iterate through 'tokens' and 'value' columns simultaneously using zip
for tokens, value in zip(data_final['tokens'], data_final['value']):
    # Lemmatize the tokens
    lemma_tokens = lemmatize_sentence(tokens)
    
    # Remove noise (stop words) from the lemma_tokens
    rm_noise = remove_noise(tokens, stop_words)
    
    # Check if rm_noise is not empty before appending
    if rm_noise and len(rm_noise) > 0:  # Check if rm_noise is not empty (length greater than 0)
        # Append the cleaned_tokens along with their corresponding 'value' to the list
        cleaned_tokens.append({'tokens': rm_noise, 'value': value})




##################### Analysis ##########################


##################### WordCloud ##########################

# Create a dictionary to store the frequency of each token
token_frequency = {}

# Iterate through the cleaned_tokens and update the token frequency
for entry in cleaned_tokens:
    token = entry['tokens'][0]  # Access the single token from the 'tokens' list
    value = entry['value']
    token_frequency[token] = token_frequency.get(token, 0) + value

#Generate WordCloud Image
keyword_wordcloud = WordCloud(width = 800, height = 800,
                              background_color = 'white',
                              min_font_size = 10).generate_from_frequencies(token_frequency)

plt.imshow(keyword_wordcloud)
plt.axis("off")
plt.show()



##################### Sentiment Analysis ##########################

sentiment_data = pd.DataFrame()

# Perform sentiment analysis for each dictionary in cleaned_tokens
text_blob = []
tokens_list = []
for entry in cleaned_tokens:
    tokens = entry['tokens']
    tokens_list.append(tokens)  # Append the tokens list to tokens_list
    
    sentiment = "Neutral"  # Default sentiment if polarity is 0 or token not found
    for token in tokens:
        analysis = TextBlob(token)
        polarity = analysis.sentiment.polarity
        if polarity > 0:
            sentiment = "Positive"
            break  # If any token has positive polarity, set sentiment to Positive and exit loop
        elif polarity < 0:
            sentiment = "Negative"
            break  # If any token has negative polarity, set sentiment to Negative and exit loop
    text_blob.append(sentiment)

# Add the 'Tokens' and 'Sentiment' columns to the 'new' DataFrame
sentiment_data['Tokens'] = tokens_list
sentiment_data['Sentiment'] = text_blob



for_sentiment_plot = sentiment_data[['Tokens','Sentiment']]
for_sentiment_plot.drop(for_sentiment_plot.loc[for_sentiment_plot['Sentiment']=='Neutral'].index, inplace=True)


# Count the occurrences of each sentiment
sentiment_counts = for_sentiment_plot['Sentiment'].value_counts()

# Create the count plot using pandas plot function
sentiment_plot = sentiment_counts.plot(kind='bar')

# Customize the plot
plt.title('Sentiment Analysis on Book Reviews')
plt.xlabel('Sentiment')
plt.ylabel('Count')

# Add annotations (frequency numbers) to the bars
for index, value in enumerate(sentiment_counts):
    plt.text(index, value, str(value), ha='center', va='bottom')



