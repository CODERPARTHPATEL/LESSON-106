import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

rating_df = pd.read_csv('ratings.csv')
rating_df.head()

movies_df= pd.read_csv('movies.csv')

movies_df.head()

movies_df['year'] = movies_df.title.str.extract(r'\((\d\d\d\d)\)', expand=True)
movies_df['year'] = movies_df.year.str.extract(r'(\d\d\d\d)', expand=True)

movies_df['title'] = movies_df.title.str.replace(r'\((\d\d\d\d)\)', '', regex=True)
movies_df['title'] = movies_df['title'].apply(lambda x: x.strip())

movies_df.head()
movies_df['genres'] = movies_df.genres.str.split('|')

movies_copy = movies_df.copy()
for index,row in movies_df.iterrows():
    for genre in row['genres']:
        movies_copy.at[index,genre]=1

movies_copy=movies_copy.fillna(0)
movies_copy.head()

ratings_df = rating_df.drop(['timestamp'],axis=1)
rating_df.head()

genre_columns = movies_copy.drop(['movieId','title','genres','year'])
genre_count = genre_columns.sum().sort_values(ascending=False)

plt.figure(figsize=(10,5))
plt.bar(genre_count.index,genre_count.value,color='#4C9AFF')
plt.title('moies per genre')
plt.xlabel('genre')
plt.ylabel('number of movies')
plt.xticks(rotation=45,ha='right')
plt.tight_layout()
plt.show()