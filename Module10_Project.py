# -*- coding: utf-8 -*-
"""
Finding the overlap in the Top100 Goodreads and NY Times Bestsellers that haven't been read
"""
import pandas as pd
import re

df_Top100 = pd.read_csv('Clean_Goodreads_Top100.csv')
df_NYT = pd.read_csv('Clean_NYTimes_Bestsellers.csv')
df_Export = pd.read_csv('goodreads_library_export.csv')

def clean_title(title):
    title_upper = title.strip().upper()
    title_b4_punc = re.match(r'^[A-Z0-9\s]+', title_upper)
    return title_b4_punc.group(0).strip() if title_b4_punc else title_upper
    
# Add a clean_title column in each data frame
df_Top100['clean_title'] = df_Top100['Title'].apply(clean_title)
df_NYT['clean_title'] = df_NYT['Title'].apply(clean_title)
df_Export['clean_title'] = df_Export['Title'].apply(clean_title)

# Match book titles in df_Top100 to df_NYT and add matches to list
matching_books = []
for idx, row in df_Top100.iterrows():
    if row['clean_title'] in df_NYT['clean_title'].values:
        matching_books.append(row)            
df_matches = pd.DataFrame(matching_books)
print(df_matches)

# Remove books from df_matches that are in df_Export
df_matches = df_matches[~df_matches['clean_title'].isin(df_Export['clean_title'])]

df_matches.to_csv('books.csv', index=False)