# An application that extract articles from Wikipedia. It transform them in a suitable format and load as csv files
# Created by Firat YASAR
# Find me at yasarigno.github.io

# Import the necessary libraries

import os
import sys
import pandas as pd
import string
from collections import Counter
import requests

import nltk
from nltk.corpus import stopwords

# Check if stopwords are already downloaded
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    # Download stopwords if not found
    nltk.download('stopwords')

# Load stopwords
stopwords = nltk.corpus.stopwords.words('english')

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
    
# Define the list of words you want to remove from the text
# stopwords = [
#     'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your',
#     'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she',
#     'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their',
#     'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that',
#     'these', 'those', 'many', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
#     'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an',
#     'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of',
#     'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into',
#     'through', 'during', 'also', 'before', 'after', 'above', 'below', 'to', 'from',
#     'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again',
#     'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how',
#     'all', 'any', 'both', 'each', 'few', 'more', 'since', 'most', 'other', 'some',
#     'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too',
#     'very', 'largest', 'smallest', 'can', 'will', 'just', 'don', 'should', 'now', 'first', 'second', 'one', 'two', 'among'
# ]
    
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

    # use a python list comprehension to remove the stopwords from words_list
    article_without_stopwords = [word for word in words_list if word not in stopwords]

    common_article = Counter(article_without_stopwords).most_common(20)

    return common_article

# Construct the column names
column_names = [f'word_{i+1}' for i in range(20)]

# Create an empty dataframe
data = []

# Create the pandas DataFrame
df = pd.DataFrame(
    data, columns=['title'] + column_names)

def load(title, common):
    """
    Appends a row to the existing CSV file or creates a new file if it doesn't exist
    """
    file_path = "data/" + "animals" + '.csv'
    
    if os.path.exists(file_path):
        # Load the existing CSV file
        df = pd.read_csv(file_path)
    else:
        # Create a new dataframe if the file doesn't exist
        df = pd.DataFrame(columns=['title'] + column_names)

    # Create a new row to append to the dataframe
    new_row = [title] + [common[index] for index in range(20)]
    
    # Append the new row to the dataframe
    df.loc[df.shape[0]] = new_row

    # Drop duplicates based on the 'title' column
    df.drop_duplicates(subset=['title'], inplace=True)
    
    # Reset the index
    df.reset_index(drop=True, inplace=True)

    # Save the updated dataframe to the CSV file
    df.to_csv(file_path, index=False)

    print (df)
    
    return df

if __name__ == "__main__":
    try:
        article = str(sys.argv[1])
        load(article, transform(article))
    except IndexError:
        print("Please provide an article title as a command-line argument and verify that it corresponds well a wikipedia article.")
    except ValueError as e:
        print(e)
        sys.exit(1)

# This app can be used in terminal by putting: python app.py "article"