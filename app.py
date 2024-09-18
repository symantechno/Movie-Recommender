import streamlit as st
import pickle
import pandas as pd
import requests

# Function to fetch poster from TMDB API
def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US')
    data = response.json()
    return 'https://image.tmdb.org/t/p/w500' + data['poster_path']

# Function to recommend movies
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

# Function to download file from Google Drive
def download_file_from_google_drive(file_id, destination):
    URL = f'https://drive.google.com/uc?id={file_id}'
    response = requests.get(URL, stream=True)
    if response.status_code == 200:
        with open(destination, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        return True
    else:
        st.error("Failed to download the file. Check the file ID and your network connection.")
        return False

# File ID of the `similarity.pkl` on Google Drive
FILE_ID = '1h6iWa7dKSBIfuhyJRgK6tknhmONdKuL-'
# Download `similarity.pkl` from Google Drive
if not download_file_from_google_drive(FILE_ID, 'similarity.pkl'):
    st.stop()  # Stop the app if the file download fails

# Load movie list and similarity matrix
try:
    movies_dict = pickle.load(open('movie_list.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)
    similarity = pickle.load(open('similarity.pkl', 'rb'))
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Streamlit app UI
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
