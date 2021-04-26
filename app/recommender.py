import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app import db

conn = db.connect()

def get_all_movies():
    # need to change limit
    movies_query = 'SELECT name, genres FROM Movie ORDER BY RAND() LIMIT 100;'
    movies = conn.execute(movies_query).fetchall()
    return movies

def get_liked_movies(user_id):
    liked_movies_query = 'SELECT name, genres FROM Review_movie NATURAL JOIN Movie WHERE user_id = {} and score >= 8;'.format(user_id)
    liked_movies = conn.execute(liked_movies_query).fetchall()
    return liked_movies

def create_df(movies):
    df = pd.DataFrame(movies, columns=['name', 'genres'])
    return df

def get_index_from_title(df, name):
    return df[df.name == name].index

def combined_features(row):
    return row['name']+" "+row['genres']

# add more features??
def get_recommendation(user_id):
    movies = get_all_movies()
    liked_movies = get_liked_movies(user_id)
    df = create_df(movies + liked_movies)
    df.fillna("", inplace = True)
    cv = CountVectorizer()
    df["combined_features"] = df.apply(combined_features, axis =1)
    count_matrix = cv.fit_transform(df["combined_features"])
    cosine_sim = cosine_similarity(count_matrix)

    movies_dict = {}
    for movie in liked_movies:
        movie_idx = get_index_from_title(df, movie[0])
        similar_movies = list(enumerate(cosine_sim[movie_idx[0]]))
        sorted_similar_movies = [movie for movie in similar_movies if movie[1] > 0.4]
        for i in range(len(sorted_similar_movies)):
            sim_movie = df.iloc[sorted_similar_movies[i][0], 0]
            if sim_movie in movies_dict:
                movies_dict[sim_movie] += 1
            else:
                movies_dict[sim_movie] = 1
    return sorted(movies_dict, key=movies_dict.get, reverse=True)[:3]
