# -*- coding: utf-8 -*-
"""
Irene Buck
11/11/25
Module 7 - Project - KMeans Clustering

"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

data = 'goodreads_library_export.csv'
df = pd.read_csv(data)
pd.options.display.max_columns=5

print(df.info())
df = df.drop(columns=['Book Id', 'Title', 'Author', 'Author l-f', 
                      'Additional Authors', 'ISBN', 'ISBN13', 'Publisher', 
                      'Binding', 'Number of Pages',
                      'Original Publication Year', 'Date Read',
                      'Date Added', 'Bookshelves', 
                      'Bookshelves with positions','Exclusive Shelf', 
                      'My Review', 'Spoiler', 'Private Notes', 
                      'Read Count', 'Owned Copies']
             )

print(df.info())
print(df.describe())

sns.displot(data=df, x='My Rating', kind='hist')
plt.title('Values in My Rating Column')
plt.show()

df = df[df['My Rating'] != 0]
df = df.reset_index(drop=True)

scaler = StandardScaler()
df = scaler.fit_transform(df)
df = pd.DataFrame(df, columns=['My Rating', 'Average Rating', 'Year Published'])
print(df)

# Visualize the data
# Create 3D visualization
fig = plt.figure(figsize=(6,6))
ax = plt.axes(projection='3d')
z = df['My Rating']
x = df['Average Rating']
y = df['Year Published']
ax.set_zlabel('My Rating')
ax.set_xlabel('Average Rating')
ax.set_ylabel('Year Published')
ax.set_title('3D Scatter Plot of Goodreads Books Read - Normalized Data')
ax.scatter(x,y,z, c=z)
plt.show()

# # Implementing KMeans
# Elbow method to determine optimal number of clusters
def optimize_k_means(data, max_k):
    means = []
    inertias = []
    
    for k in range(2, max_k):
        kmeans = KMeans(n_clusters=k)
        kmeans.fit(data)
        
        means.append(k)
        inertias.append(kmeans.inertia_)
        
    fig = plt.subplots(figsize=(10,5))
    plt.plot(means, inertias, 'o-')
    plt.xlabel('Number of Clusters')
    plt.ylabel('Inertia')
    plt.grid(True)
    plt.show()
    
optimize_k_means(df[['My Rating', 'Average Rating']], 10)

# KMeans on object with 2, 3, and 4 clusters

for n in range(2, 5):
    initKMeans = KMeans(n_clusters=n)
    # Trains/fits the KMeans algo to the df, interating through the data and recalculating centers
    myKMeans = initKMeans.fit(df)
    
    # Get cluster assignment for each vector/person
    cluster_labels = myKMeans.labels_
    print(cluster_labels)
    
    # Get the cluster centers AKA centroids
    centroids = myKMeans.cluster_centers_
    print(centroids)
    
    # Compare the actual Survived column to the Kmeans outcome
    print(pd.Series(cluster_labels).value_counts())
    
    # Create 3D visualization
    fig = plt.figure(figsize=(6,6))
    ax = plt.axes(projection='3d')
    z = df['My Rating']
    x = df['Average Rating']
    y = df['Year Published']
    ax.set_zlabel('My Rating')
    ax.set_xlabel('Average Rating')
    ax.set_ylabel('Year Published')
    ax.set_title('3D Scatter Plot of Goodreads Books Read - Normalized Data')
    ax.scatter(x,y,z, c=z)
    ax.scatter(centroids[:, 0], centroids[:, 1],centroids[:,2], c = 'red', marker='X', s=400)
    plt.show()

    # Predict Survival of new person
    new_book_data = [[.5, 1, .6]]
    new_book_np = np.array(new_book_data).reshape(1,-1)
    test_df = pd.DataFrame(new_book_np)
    prediction_myKMeans = myKMeans.predict(test_df)
    print(f'My KMeans predicts the new book would be in the {prediction_myKMeans} group.')