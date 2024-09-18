import streamlit as st
import pickle
import pandas as pd
import requests
import gdown

# Function to download files from Google Drive
def download_file_from_google_drive(file_id, output_file):
    url = f'https://drive.google.com/uc?id={file_id}'
    gdown.download(url, output_file, quiet=False)

# Replace these with the actual Google Drive file IDs
movie_list_file_id = 'your_movie_list_file_id_here'
similarity_file_id = 'your_similarity_file_id_here'

# Download the files from Google Drive
download_file_from_google_drive(movie_list_file_id, 'movie_list.pkl')
download_file_from_google_drive(similarity_file_id, 'similarity.pkl')

# Load the files after downloading
movies_dict = pickle.load(open('movie_list.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US')
    data = response.json()
    return 'https://image.tmdb.org/t/p/w500' + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommend_movies = []
    recommend_movies_posters = []
    for i in movies_list:
        movie_id = (movies.iloc[i[0]].movie_id)
        recommend_movies.append(movies.iloc[i[0]].title)
        recommend_movies_posters.append(fetch_poster(movie_id))
    return recommend_movies, recommend_movies_posters

st.title('Movie Recommendation System')

selected_movie = st.selectbox(
    'Choose a movie to get recommendations:',
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    l = [col1, col2, col3, col4, col5]

    for i, j, k in zip(names, posters, range(5)):
        with l[k]:
            st.text(i)  
            st.image(j)
