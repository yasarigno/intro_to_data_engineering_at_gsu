# An application that extract articles from Wikipedia. It transform them in a suitable format and load as csv files
# Created by Firat YASAR
# Find me at yasarigno.github.io

import sys
import requests

import pandas as pd
from collections import Counter

def extract(article):
    '''
    This function returns the raw text of a wikipedia page 
    given a wikipedia page title
    '''
    params = { 
        'action': 'query', 
        'format': 'json', # request json formatted content
        'titles': article, # title of the wikipedia page
        'prop': 'extracts', 
        'explaintext': True
    }
    # send a request to the wikipedia api 
    response = requests.get(
         'https://en.wikipedia.org/w/api.php',
         params= params
     ).json()

    # Parse the result
    page = next(iter(response['query']['pages'].values()))
    # return the page content 
    if 'extract' in page.keys():
        return page['extract']
    else:
        return "Page not found"
    
# define the list of words you want to remove from the text
# stopwords = ['the', 'of', 'and', 'is','to','in','a','from','by','that', 'with', 'this', 'as', 'an', 'are','its', 'at', 'for']

import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
stopwords = stopwords.words('english')

    
def transform (article):
    """
    Takes a text
    Removes stopwords
    Find the most common 20 words in it
    Returns a list of words together with their frequency
    """
    article_received = extract(article).lower()
    # by splitting over the space character ' '
    words_list = article_received.split(' ')

    # and count the words
    article_word_counts = Counter(words_list)

    # use a python list comprehension to remove the stopwords from words_list
    article_without_stopwords = [word for word in words_list if word not in stopwords]

    common_article = Counter(article_without_stopwords).most_common(20)

    return common_article

# Create an empty dataframe
# Initialize list of lists
data = []

# Create the pandas DataFrame
df = pd.DataFrame(
    data, columns=['title', 'common_words'])

def load (title, common):
    """
    Adds a row to the dataframe data
    Loads the result as a csv file
    """
    df.loc[df.shape[0]] = [title, common]
    df.drop_duplicates(subset=['title'],inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.to_csv(title + '.csv')
    return df

if __name__ == "__main__":
    article = str(sys.argv[1])
    load(article, transform (article))

# This app can be used in terminal by putting: python app.py "article"


