import pandas as pd
import pickle
import requests


movies_dict=pickle.load(open('movie_dict.pkl','rb'))
final_table=pd.DataFrame(movies_dict)

similarity=pickle.load(open('similarity.pkl','rb'))

#function to fetch details of the recommended movie
def fetch_details(movie_name):
    url = "http://www.omdbapi.com/?apikey=1f9835b2&t="+movie_name
    data = requests.get(url)
    data = data.json()
    movie_details=[]
    if data['Response']=="True":
        movie_poster = data['Poster']
        movie_details.append({
            'title': movie_name,
            'released': data['Released'],
            'genre': data['Genre'],
            'director': data['Director'],
            'actors': data['Actors'],
            'plot': data['Plot'],
            "poster": movie_poster
        })
    else:
        movie_poster = "http://www.filmfodder.com/reviews/images/poster-not-available.jpg"
        movie_details.append({
            'title': movie_name,
            'released': "No info",
            'genre': "No info",
            'director': "No info",
            'actors': "No info",
            'plot': "No info",
            "poster": movie_poster
        })
    return movie_details

#function to return the recommended movies along with their details
def recom(movie):
    movie_index=final_table[final_table['title']==movie].index[0]
    distances=similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:7]
    req_list=[]
    for i in movies_list:
        req_list.append(fetch_details(final_table.iloc[i[0]].title)) ## i=(index,distance)
    return req_list

#function to return list of movies
def getmovies():
    movie_lis = final_table['title'].values
    return movie_lis