import streamlit as st
import pickle
import pandas as pd
import requests
from functools import lru_cache

@lru_cache(maxsize=1000)
def fetch_poster(movie_id):
    base_url = "https://image.tmdb.org/t/p/w500"
    api_url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=420b8821330cec3f214163c75423281c'
    
    try:
        response = requests.get(api_url, timeout=2)
        data = response.json()
        poster_path = data.get('poster_path')
        return f"{base_url}{poster_path}" if poster_path else None
    except:
        return None

# Load movies data
movies_list = pickle.load(open('movies.pkl', 'rb'))
if isinstance(movies_list, pd.DataFrame):
    movies = movies_list
else:
    movies = pd.DataFrame(movies_list)

# Ensure 'title' column exists
if 'title' not in movies.columns:
    st.error("Error: 'title' column not found in the movies data.")
    st.stop()

# Load similarity matrix
similarity = pickle.load(open('similarity.pkl', 'rb'))

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    recommended_movies_posters = []
    
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        poster = fetch_poster(movie_id)
        recommended_movies_posters.append(poster if poster else "https://via.placeholder.com/500x750.png?text=No+Poster")
    
    return recommended_movies, recommended_movies_posters

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    "Select a movie", movies['title'].tolist())


if st.button("Get Recommendations"):
    names,posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])
