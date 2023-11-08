import reflex as rx
import pickle
import pandas as pd
import requests


class MovieState(rx.State):
    movie_dict: dict = pickle.load(open("/home/heet/Work/Development/reflex-movie-recommendation/ReflexRave/ReflexRave/movie_dict.pkl", "rb"))
    movies: list = list(movie_dict["title"].values())
    show: bool = False
    selected_movie: str
    recommended_movies: list = []
    recommended_movies_poster: list = []
    recommendation: list = []

    def fetch_poster(self, movie_id):
        response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=<YOUR_TMDB_API_KEY>'.format(movie_id))
        data = response.json()
        poster_url = 'https://image.tmdb.org/t/p/w500/' + data['poster_path']
        return poster_url

    def predict(self):
        self.recommended_movies = []
        self.recommended_movies_poster = []

        similarity = pickle.load(open('/home/heet/Work/Development/reflex-movie-recommendation/ReflexRave/ReflexRave/similarity.pkl', 'rb'))

        movies = pd.DataFrame(self.movie_dict)
        movie_index = movies[movies['title'] == self.selected_movie].index[0]
        distance = similarity[movie_index]
        movies_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:7]

        
        for i in movies_list:
            movie_id = movies.iloc[i[0]].movie_id
            self.recommended_movies.append(movies.iloc[i[0]].title)
            poster_url = self.fetch_poster(movie_id)
            self.recommended_movies_poster.append(poster_url)

        self.show = True
