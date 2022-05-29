import numpy as np
import pandas as pd
import ast

movies=pd.read_csv('tmdb_5000_movies.csv')
credits=pd.read_csv('tmdb_5000_credits.csv')

movies=movies.merge(credits,on='title')

#recommendation on the basis of genre,keyword,overview,cast,director
#keep id,title
movies=movies[['movie_id','title','overview','genres','keywords','cast','crew']]
movies.dropna(inplace=True)

#function to fetch name of the attributes
def convert(text):
    L=[]
    for i in ast.literal_eval(text):
        L.append(i['name'])
    return L
movies['genres']=movies['genres'].apply(convert)
movies['keywords']=movies['keywords'].apply(convert)

#function to fetch top 3 cast of the movie
def top3cast(text):
    L=[]
    ctr=0
    for i in ast.literal_eval(text):
        if ctr<3:
            L.append(i['name'])
            ctr+=1
        else:
            break
    return L
movies['cast']=movies['cast'].apply(top3cast)

#function to fetch director of the movie
def fetch_director(text):
    L=[]
    for i in ast.literal_eval(text):
        if i['job']=='Director':
            L.append(i['name'])
            break
    return L
movies['crew']=movies['crew'].apply(fetch_director)

#coverting overview in a list to concatenate it with other lists
movies['overview']=movies['overview'].apply(lambda x:x.split())

#removing space to make recommendation more accurate
movies['genres']=movies['genres'].apply(lambda x:[i.replace(" ","") for i in x])
movies['keywords']=movies['keywords'].apply(lambda x:[i.replace(" ","") for i in x])
movies['cast']=movies['cast'].apply(lambda x:[i.replace(" ","") for i in x])
movies['crew']=movies['crew'].apply(lambda x:[i.replace(" ","") for i in x])

#merging coloumns for final comparision
movies['tags']=movies['overview']+movies['genres']+movies['keywords']+movies['cast']+movies['crew']

final_table=movies[['movie_id','title','tags']]
final_table['tags']=final_table['tags'].apply(lambda x:" ".join(x))
final_table['tags']=final_table['tags'].apply(lambda x:x.lower())

#####     TEXT VECTORIZATION    ######

from sklearn.feature_extraction.text import CountVectorizer
cv=CountVectorizer(max_features=5000,stop_words='english')
vectors=cv.fit_transform(final_table['tags']).toarray()

import nltk
from nltk.stem.porter import PorterStemmer
ps=PorterStemmer()

def stem(text):
    y=[]
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)

final_table['tags']=final_table['tags'].apply(stem)

from sklearn.metrics.pairwise import cosine_similarity
similarity=cosine_similarity(vectors)

import pickle
pickle.dump(final_table.to_dict(),open('movie_dict.pkl','wb'))
pickle.dump(similarity,open('similarity.pkl','wb'))

