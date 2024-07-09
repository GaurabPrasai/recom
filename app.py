import streamlit as st
import pickle
import pandas as pd
import os

st.title('Movie Recommender System')

def load_data(filename):
    if not os.path.exists(filename):
        st.error(f"Error: The file '{filename}' does not exist.")
        return None
    
    try:
        with open(filename, 'rb') as file:
            data = pickle.load(file)
        return data
    except Exception as e:
        st.error(f"Error loading {filename}: {str(e)}")
        return None

# Load movies data
movies_list = load_data('movies.pkl')
if movies_list is None:
    st.stop()

if isinstance(movies_list, pd.DataFrame):
    movies = movies_list
else:
    movies = pd.DataFrame(movies_list)

# Ensure 'title' column exists
if 'title' not in movies.columns:
    st.error("Error: 'title' column not found in the movies data.")
    st.stop()

# Load similarity matrix
similarity = load_data('similarity.pkl')
if similarity is None:
    st.stop()

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    for i in movie_list:
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies

selected_movie_name = st.selectbox(
    "Select a movie", movies['title'].tolist())

if st.button("Get Recommendations"):
    try:
        recommendations = recommend(selected_movie_name)
        for i in recommendations:
            st.write(i)
    except Exception as e:
        st.error(f"An error occurred while getting recommendations: {str(e)}")

st.info("If you're experiencing issues, please check that your 'movies.pkl' and 'similarity.pkl' files are up to date and compatible with your current Python version.")