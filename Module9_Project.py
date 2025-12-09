# -*- coding: utf-8 -*-
"""
Irene Buck
11/24/25
Module 9 - Project - Decision Tree Modelling
"""
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report

# Format the Data
df = pd.read_csv("Clean_Goodreads_Top100.csv")
pd.options.display.max_columns=10
print(df.head())

df = df.drop(columns=['Title', 'Authors', 'Description', 'Page Count', 'Genres'])
print(df)

df['Label'] = df['Star Score']
df['Label'] = df['Label'].astype(str)

df.loc[df['Star Score'] < 4.11, 'Label'] = 'Good'
df.loc[(df['Star Score'] < 4.25) & (df['Star Score'] > 4.10), 'Label'] = 'Better'
df.loc[df['Star Score'] >= 4.25, 'Label'] = 'Best'
print(df['Label'].value_counts())        
df = df.drop(columns=['Star Score'])

rating_condition = df['Rating Count'] < 500
review_condition = df['Reviews Count'] < 200
df = df[~rating_condition]
df = df[~review_condition]
print(df)
print(df.info())

Y = df['Label']   # We are predicting Survival based on Sex, Age, and Fare
X = df.drop(columns=['Label'])
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, random_state = 3, test_size=.3)
print(X_train.head())
print(Y_train.head())
print(X_test.head())
print(Y_test.head())
print(X_train.shape)
print(Y_train.shape)
print(X_test.shape)
print(Y_test.shape)


# Visualize the Data
plt.figure(figsize=(6, 6))
sns.barplot(x=Y_train.value_counts().index, y=Y_train.value_counts(), hue=Y_train.value_counts()) 
plt.title('Star Score Lables in Training Data')
plt.ylabel('Count')
plt.xlabel('Label')
plt.show()

sns.relplot(data=X_train, y='Rating Count', x='Reviews Count', kind='line')
plt.show()

sns.catplot(data=X_train, x='Publication Year', kind='violin')
plt.show()

# Apply Decision Tree modeling
clf = DecisionTreeClassifier(min_samples_split=10)
clf = clf.fit(X_train, Y_train)

##Tree Plot Option 1
MyPlot=tree.plot_tree(clf,
                   feature_names=X_train.columns, 
                   class_names=clf.classes_,
                   filled=True)
## To see the tree, open this file in CS 332 folder
plt.savefig("MyProjectTree.jpg")
plt.close()

Prediction=clf.predict(X_test)
print(Prediction)

label_names= ['Good', 'Better', 'Best']

Actual_Labels = Y_test
Predicted_Labels = Prediction

##Create the Basic Confusion Matrix as a heatmap in Seaborn.
## Note that you can also use Sklearn's ConfusionMatrixDisplay
My_Conf_Mat = confusion_matrix(Actual_Labels, Predicted_Labels)
print(My_Conf_Mat)
##Create the fancy CM using Seaborn
sns.heatmap(My_Conf_Mat, annot=True,cmap='Blues',xticklabels=label_names, yticklabels=label_names, cbar=False)
plt.title("Confusion Matrix For Goodreads Top100 Nonfiction Test Data",fontsize=20)
plt.xlabel("Predicted", fontsize=15)
plt.ylabel("Actual", fontsize=15)
plt.show()

# Calculate the accuracy, 67% of the time the prediction is accurate
print(accuracy_score(Y_test, Prediction))
# Shows accuracy at multiple iterations of training
print(cross_val_score(clf, X_train, Y_train, cv=10))
# breaks down the accuracy for each value and more
print(classification_report(Prediction, Y_test))