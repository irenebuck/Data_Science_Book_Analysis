# -*- coding: utf-8 -*-
"""
Created on Tue Oct 14 14:21:34 2025

@author: Irene
"""

# key for API 6OKOlzD0cmYHtDsAsOC9oGE0GZH9gPF4

import datetime
import requests
import csv
from time import sleep

start_date = datetime.date(2015, 1, 4)   # First end of week(Sunday) in 2015
end_date = datetime.date(2019, 12, 31)
current_date = start_date
csv_file = 'nytimes_bestsellers.csv'


def format_date(a_date):
    """
    Takes the date in the datetime.data() format and returns the same date
    as a string in the YYYY-MM-DD format required for the API call
    """
    formatted_date = a_date.strftime("%Y-%m-%d")
    return formatted_date


def pull_book_data(parsed_json):
    """
    Takes the JSON response the API provided, pulls only the fiction and 
    non-fiction bestseller lists(the first 2 lists), pulls some of the book
    details, and appends them to a books list. 
    Returns the books list
    """
    books = []
    for book in parsed_json['results']['books']:
        book_details = {
            'list_publish_date': parsed_json['results']['published_date'],
            'amazon_product_url': book['amazon_product_url'],
            'author': book['author'],
            'description': book['description'],
            'primary_isbn13': book['primary_isbn13'],
            'rank': book['rank'],
            'rank_last_week': book['rank_last_week'],
            'title': book['title'],
            'weeks_on_list': book['weeks_on_list']
            }
        books.append(book_details)
    return books

column_names = ['list_publish_date','amazon_product_url','author',
                'description','primary_isbn13','rank','rank_last_week','title',
                'weeks_on_list']

with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=column_names)
    writer.writeheader()

while current_date <= end_date:  
    list_date = format_date(current_date)
    list_name = 'hardcover-nonfiction'
    url = f'https://api.nytimes.com/svc/books/v3/lists/{list_date}/{list_name}.json?api-key=6OKOlzD0cmYHtDsAsOC9oGE0GZH9gPF4'
    response = requests.get(url)
    data = response.json()
    bookdata = pull_book_data(data)

    with open(csv_file, 'a', newline='') as file:
        writer = csv.DictWriter(file,fieldnames=column_names)
        writer.writerows(bookdata)
        file.close()
    
    current_date += datetime.timedelta(weeks=1)
    sleep(12)

    
    
