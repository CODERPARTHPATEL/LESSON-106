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

genre_columns = movies_copy.drop(['movieId','title','genres','year'],axis=1)
genre_count = genre_columns.sum().sort_values(ascending=False)

plt.figure(figsize=(10,5))
plt.bar(genre_count.index,genre_count.values,color='#4C9AFF')
plt.title('moies per genre')
plt.xlabel('genre')
plt.ylabel('number of movies')
plt.xticks(rotation=45,ha='right')
plt.tight_layout()
plt.show()

user_input = [
    {'title':'Grand Slam','rating':5.6},
    {'title':'Zero','rating':7},
    {'title':'Jumanji','rating':8.5},
    {'title':'Toy Story','rating':4.5},
]
movies_input = pd.DataFrame(user_input)
movies_input

input_id = movies_df[movies_df['title'].isin(movies_input['title'].tolist())]
movies_input = pd.merge(input_id,movies_input)
movies_input = movies_input.drop(['genres','year'],axis=1)
movies_input

movies_user = movies_copy[movies_copy['movieId'].isin(movies_input['movieId'].tolist())]
movies_user = movies_user.reset_index(drop=True)

UserGenreTable = movies_user.drop(['movieId','title','genres','year'],axis=1)

UserProfile = UserGenreTable.transpose().dot(movies_input['rating'])
UserProfile

plt.figure(figsize=(10,5))
plt.bar(UserProfile.index,UserProfile.values,color='#FF6B6B')
plt.title('your taste profile')
plt.xlabel('genre')
plt.ylabel('weight')
plt.xticks(rotation=45,ha='right')
plt.tight_layout()
plt.show()



GenreTable =  movies_copy.set_index(movies_copy['movieId'])
GenreTable = GenreTable.drop(['movieId','title','genres','year'],axis=1)

Recomendation_df = ((GenreTable*UserProfile).sum(axis=1)/UserProfile.sum())
Recomendation_df = Recomendation_df.sort_values(ascending=False)
Recomendation_df.head()


top20_ids = Recomendation_df.head(20).index

Recomendation_table = movies_df[

movies_df['movieId'].isin(top20_ids)

]

Recomendation_table


top10_scores = Recomendation_df.head(10)
top10_titles = movies_df.set_index('movieId').loc[top10_scores.index]['title']


plt.figure(figsize=(8,6))
plt.barh(top10_titles[::-1],top10_scores.values[::-1],color='#51CF66')
plt.title('top 10 picks')
plt.xlabel('match score')
plt.tight_layout()
plt.show()