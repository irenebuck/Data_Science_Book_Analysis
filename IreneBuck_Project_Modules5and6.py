# -*- coding: utf-8 -*-
"""
Irene Buck
10/31/25
Modules 5 and 6
Project - Data Cleaning
"""
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

dfNY = pd.read_csv("nytimes_bestsellers.csv")
dfGR = pd.read_csv("goodreads_top100_from1980to2023_final.csv")

# Cleaning the Goodreads Top100 dataset
print(dfGR.info())
dfGR = dfGR.drop(columns=['Unnamed: 0','isbn','series_title', 'series_release_number', 'publisher',
                          'language', 'format', 'url', 'current_readers', 
                          'want_to_read', 'price'])
print(dfGR.info())
print(dfGR['num_pages'].unique())
print(dfGR['publication_date'].value_counts())
print(dfGR.describe())

dfGR = dfGR.drop_duplicates(subset=['title', 'authors'], keep='last')

dfGR = dfGR.dropna(subset=['publication_date'])
dfGR = dfGR.reset_index(drop=True)

dfGR['num_pages'] = dfGR['num_pages'].str.split().str[0]
dfGR['num_pages'] = pd.to_numeric(dfGR['num_pages'], errors='coerce') 
mean_avg = int(dfGR['num_pages'].mean())
dfGR['num_pages'] = dfGR['num_pages'].fillna(mean_avg)

dfGR['num_pages'] = dfGR['num_pages'].astype(int)
dfGR['num_ratings'] = dfGR['num_ratings'].astype(int)
dfGR['num_reviews'] = dfGR['num_reviews'].astype(int)
dfGR['publication_date'] = dfGR['publication_date'].str.slice(-4)
dfGR['publication_date'] = pd.to_numeric(dfGR['publication_date'], errors='coerce')

for i in range(len(dfGR)-1,-1,-1):
    item = dfGR.loc[i]
    remove = False
    
    pages, pub, rate, genre = item['num_pages'], item['publication_date'], item['rating_score'], item['genres']
    
    if not(0<pages<1000 and pub>2000 and rate>4.0):
        remove = True
    elif not("Nonfiction" in genre):
        remove = True
    
    if remove:
        dfGR = dfGR.drop(i)

dfGR = dfGR.reset_index(drop=True)

dfGR.to_csv('Clean_Goodreads_Top100.csv', header=['Title', 'Authors', 'Description', 'Page Count', 'Genres', 
        'Publication Year', 'Star Score', 'Rating Count', 'Reviews Count'], index=False)

print(dfGR.info())
plt.figure(figsize=(8,6)) 
plt.bar(dfGR['publication_date'].value_counts().index, dfGR['publication_date'].value_counts().values, color='pink')
plt.title("Goodreads Top 100 Nonfiction Published Each Year")
plt.ylabel('Count')
plt.xlabel('Years')
plt.show()

new_df = dfGR[['publication_date','num_pages', 'num_ratings', 'num_reviews']]
print(new_df)
normalized_data = MinMaxScaler().fit_transform(new_df[['publication_date','num_pages', 'num_ratings', 'num_reviews']])
normalized_df = pd.DataFrame(normalized_data, columns=['publication_date','num_pages', 'num_ratings', 'num_reviews'])
print(normalized_df)

new_df.to_csv('Kmeans_Goodreads.csv', index=False, index_label=False)
print(new_df)


# Cleaning the New York Times Nonfiction Bestsellers dataset
print(dfNY.info())
dfNY = dfNY.drop(columns=['amazon_product_url', 'primary_isbn13', 'rank_last_week'])
print(dfNY.info())
plt.figure(figsize=(8,6))

# Visualizes the count for each rank score
plt.bar(dfNY['rank'].value_counts().index, dfNY['rank'].value_counts().values, color='green')
plt.title("Rankings Counts")
plt.ylabel('Counts')
plt.xlabel('Rankings')
plt.show()

print(dfNY['weeks_on_list'].unique())

dfNY['list_publish_date'] = pd.to_datetime(dfNY['list_publish_date'], format='mixed')

dfNY = dfNY.groupby(['title', 'author', 'description'], as_index=False).agg({
    'list_publish_date' : 'first',
    'rank' : 'min',
    'weeks_on_list' : 'max'})

dfNY = dfNY.reset_index(drop=True)

dfNY.to_csv('Clean_NYTimes_Bestsellers.csv', header=['Title', 'Authors', 
              'Description', 'First Day On List', 'Highest Rank', 
              "Weeks On List"], index=False)

print(dfNY.info())

ny_quant = dfNY[['rank', 'weeks_on_list']]
print(ny_quant)
normal_data = MinMaxScaler().fit_transform(ny_quant[['rank', 'weeks_on_list']])
normal_df = pd.DataFrame(normal_data, columns=['rank', 'weeks_on_list'])
print(normal_df)

ny_quant.to_csv('Kmeans_NYTimes.csv', index=False, index_label=False)
print(ny_quant)

