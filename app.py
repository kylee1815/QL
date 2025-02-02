import pickle
import streamlit as st
from tmdbv3api import Movie, TMDb


movie = Movie()
tmdb = TMDb()
tmdb.api_key = 'e7eedc1b8611539fe9dbe1668887f2b1'
tmdb.language = 'ko_KR'

def get_recom(title):
    idx = movies[movies['title'] == title].index[0]

    # Get the pairwsie similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar movies
    sim_scores = sim_scores[1:11]

    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]

    # Return the top 10 most similar movies
    images = []
    titles = []
    for i in movie_indices:
        id = movies['id'].iloc[i]
        details = movie.details(id)
        
        image_path = details['poster_path']
        if image_path:
            image_path = 'https://image.tmdb.org/t/p/w500' + image_path
        else:
            image_path = 'bok.jpeg'

        images.append(image_path)
        titles.append(details.title)
    return images, titles

movies = pickle.load(open('movies.pickle', 'rb'))
cosine_sim = pickle.load(open('cosine_sim2.pickle', 'rb'))

st.set_page_config(layout="wide", page_title="Movie Recommendation System")
st.header('Kyufix')

movie_list = movies['title'].values
title = st.selectbox('Choose your movie', movie_list)
if st.button('Recommend'):
    with st.spinner('Wait!'):
        images, titles = get_recom(title)

        idx = 0
        for i in range(0,2):
            cols = st.columns(5)
            for col in cols:
                col.image(images[idx], width=500)
                col.write(titles[idx])
                idx += 1
