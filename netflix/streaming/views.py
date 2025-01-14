from django.shortcuts import get_object_or_404, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Movie, Playlist, Recommendation
from .serializers import MovieSerializer, PlaylistSerializer, RecommendationSerializer
from django.shortcuts import render
from .models import Movie, Playlist
import requests
import random
from django.conf import settings
from django.shortcuts import render
from django.db.models import Q  # For complex queries
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Movie, Playlist, Recommendation, Series
from .serializers import MovieSerializer, PlaylistSerializer, RecommendationSerializer, SeriesSerializer
from django.shortcuts import render
import requests
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404



# Function-based views
def movie_details(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    serializer = MovieSerializer(movie)
    return Response(serializer.data)


def popular_movies(request):
    # Dummy implementation, replace with actual logic
    movies = Movie.objects.filter(rating__gte=8.0)[:100]
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)


# Class-based views
class RecommendationView(APIView):
    def get(self, request, movie_id):
        recommendation = get_object_or_404(Recommendation, movie_id=movie_id)
        serializer = RecommendationSerializer(recommendation)
        return Response(serializer.data)


class MovieListView(APIView):
    def get(self, request):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MovieDetailView(APIView):
    def get(self, request, movie_id):
        movie = get_object_or_404(Movie, id=movie_id)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)


def home(request):
    # Poblar la base de datos si está vacía
    if Movie.objects.count() < 100:
        populate_movies()
    if Series.objects.count() == 0:
        populate_series()

    # Fetch the top 100 movies sorted by rating
    movies = Movie.objects.all().order_by('-rating')[:100]

    # Fetch IDs of movies in the user's playlist
    if request.user.is_authenticated:
        playlist, _ = Playlist.objects.get_or_create(user=request.user)
        playlist_movie_ids = list(playlist.movies.values_list("id", flat=True))
    else:
        playlist_movie_ids = []


    return render(request, 'streaming/home.html', {
        'movies': movies,
        'playlists': playlist_movie_ids,  # Pass only movie IDs
    })



@login_required
def playlist(request):
    # Obtiene o crea la playlist del usuario
    playlist, created = Playlist.objects.get_or_create(user=request.user)

    # Obtiene los IDs de películas y series en la playlist
    playlist_movie_ids = list(playlist.movies.values_list("id", flat=True))
    playlist_series_ids = list(playlist.series.values_list("id", flat=True))

    return render(request, 'streaming/playlist.html', {
        'playlist': playlist,
        'playlist_movie_ids': playlist_movie_ids,
        'playlist_series_ids': playlist_series_ids,
    })





def movie_details_page(request, movie_id):
    # Fetch the movie from the database
    movie = get_object_or_404(Movie, id=movie_id)
    return render(request, "streaming/movie_details.html", {"movie": movie})


def search_movies(request):
    query = request.GET.get('q', '')  # Captura el término de búsqueda
    movies = []

    if query:  # Asegúrate de que hay un término de búsqueda
        # Llamada a la API de TMDB
        api_url = "https://api.themoviedb.org/3/search/movie"
        params = {
            'api_key': settings.TMDB_API_KEY,  # Tu clave API
            'language': 'en-US',
            'query': query,  # Término de búsqueda
            'page': 1,
            'include_adult': False
        }
        response = requests.get(api_url, params=params)

        if response.status_code == 200:  # La respuesta fue exitosa
            movies = response.json().get('results', [])  # Extrae los resultados
        else:
            print(f"Error in TMDB API call: {response.status_code}")

    # Obtener IDs de películas en la playlist del usuario
    if request.user.is_authenticated:
        playlist, _ = Playlist.objects.get_or_create(user=request.user)
        playlist_movie_ids = list(playlist.movies.values_list("id", flat=True))
    else:
        playlist_movie_ids = []

    # Renderiza los resultados en el template
    return render(request, 'streaming/search_results.html', {
        'movies': movies,
        'query': query,
        'playlists': playlist_movie_ids,  # IDs de las películas en la playlist
    })




def add_to_playlist(request, content_id, content_type):
    if request.method == 'POST':
        # Get or create the user's playlist
        playlist, _ = Playlist.objects.get_or_create(user=request.user)

        # Determinar si es una película o serie
        if content_type == 'movie':
            try:
                content = Movie.objects.get(id=content_id)
            except Movie.DoesNotExist:
                # Fetch movie details from TMDB API
                api_url = f"https://api.themoviedb.org/3/movie/{content_id}"
                params = {'api_key': settings.TMDB_API_KEY, 'language': 'en-US'}
                response = requests.get(api_url, params=params)

                if response.status_code == 200:
                    data = response.json()
                    content = Movie.objects.create(
                        id=content_id,
                        title=data['title'],
                        description=data['overview'],
                        release_date=data['release_date'],
                        genre=', '.join([genre['name'] for genre in data['genres']]),
                        rating=data['vote_average'],
                        poster_path=data['poster_path'],
                    )
                else:
                    return redirect('home')  # Handle API failure
        elif content_type == 'series':
            try:
                content = Series.objects.get(id=content_id)
            except Series.DoesNotExist:
                # Fetch series details from TMDB API
                api_url = f"https://api.themoviedb.org/3/tv/{content_id}"
                params = {'api_key': settings.TMDB_API_KEY, 'language': 'en-US'}
                response = requests.get(api_url, params=params)

                if response.status_code == 200:
                    data = response.json()
                    content = Series.objects.create(
                        id=content_id,
                        title=data['name'],
                        description=data['overview'],
                        release_date=data['first_air_date'],
                        genre=', '.join([genre['name'] for genre in data['genres']]),
                        rating=data['vote_average'],
                        poster_path=data['poster_path'],
                    )
                else:
                    return redirect('home')  # Handle API failure
        else:
            return redirect('home')  # Handle invalid content type

        # Toggle the content in the playlist
        if content_type == 'movie':
            if content in playlist.movies.all():
                playlist.movies.remove(content)  # Remove movie
            else:
                playlist.movies.add(content)  # Add movie
        elif content_type == 'series':
            if content in playlist.series.all():
                playlist.series.remove(content)  # Remove series
            else:
                playlist.series.add(content)  # Add series

    return redirect(request.META.get('HTTP_REFERER', '/'))



def populate_movies():
    """
    Fetch and save the top 100 popular movies from TMDB to the database.
    """
    for page in range(1, 6):  # Fetch up to 5 pages of movies (20 movies per page = 100 movies)
        api_url = "https://api.themoviedb.org/3/movie/popular"
        params = {
            'api_key': settings.TMDB_API_KEY,
            'language': 'en-US',
            'page': page,
        }
        response = requests.get(api_url, params=params)
        if response.status_code == 200:
            popular_movies = response.json().get('results', [])
            for movie in popular_movies:
                # Avoid duplicates by using get_or_create
                Movie.objects.get_or_create(
                    id=movie['id'],
                    defaults={
                        'title': movie.get('title', 'Unknown Title'),
                        'description': movie.get('overview', 'No description available.'),
                        'release_date': movie.get('release_date', 'Unknown Date'),
                        'genre': ', '.join([genre['name'] for genre in movie.get('genres', [])]) if 'genres' in movie else 'Unknown',
                        'rating': movie.get('vote_average', 0),
                        'poster_path': movie.get('poster_path', ''),
                    },
                )
        else:
            print(f"Failed to fetch page {page}. Status code: {response.status_code}")


from django.shortcuts import render

# Views for series

def series_details_page(request, series_id):
    series = get_object_or_404(Series, id=series_id)
    return render(request, "streaming/series_details.html", {"series": series})

def search_series(request):
    query = request.GET.get('q', '')  # Captura el término de búsqueda
    series_list = []

    if query:  # Asegúrate de que hay un término de búsqueda
        # Llamada a la API de TMDB
        api_url = "https://api.themoviedb.org/3/search/tv"
        params = {
            'api_key': settings.TMDB_API_KEY,  # Tu clave API
            'language': 'en-US',
            'query': query,  # Término de búsqueda
            'page': 1,
            'include_adult': False
        }
        response = requests.get(api_url, params=params)

        if response.status_code == 200:  # La respuesta fue exitosa
            series_list = response.json().get('results', [])  # Extrae los resultados
        else:
            print(f"Error in TMDB API call: {response.status_code}")

    # Mapea las claves necesarias para el template
    formatted_series_list = [
        {
            'id': series.get('id'),
            'title': series.get('name', 'No Title Available'),  # `name` para series
            'release_date': series.get('first_air_date', 'No Date Available'),  # `first_air_date` para series
            'overview': series.get('overview', 'No Description Available'),  # `overview` para la descripción
            'poster_path': series.get('poster_path', ''),  # `poster_path` para la imagen
        }
        for series in series_list
    ]

    # Obtener IDs de las series en la playlist del usuario
    if request.user.is_authenticated:
        playlist, _ = Playlist.objects.get_or_create(user=request.user)
        playlist_series_ids = list(playlist.series.values_list("id", flat=True))
    else:
        playlist_series_ids = []

    # Renderiza los resultados en el template
    return render(request, 'streaming/search_results_series.html', {
        'series_list': formatted_series_list,
        'query': query,
        'playlists': playlist_series_ids,  # IDs de las series en la playlist
    })

 
def series_page(request):
    # Poblar la base de datos si está vacía
    if Series.objects.count() == 0:
        populate_series()

    # Obtener todas las series
    all_series = Series.objects.all().order_by('-rating')

    # Obtener la playlist del usuario si está autenticado
    playlists_series_ids = []
    if request.user.is_authenticated:
        playlist, _ = Playlist.objects.get_or_create(user=request.user)
        playlists_series_ids = list(playlist.series.values_list("id", flat=True))  # IDs de series en la playlist

    # Pasar las series y las playlists al template
    return render(request, 'streaming/series.html', {
        'series': all_series,
        'playlists': playlists_series_ids,  # IDs de series en la playlist
    })





def populate_series():
    """
    Fetch and save the top 100 popular TV series from TMDB to the database.
    """
    for page in range(1, 6):  # Fetch up to 5 pages of series (20 series per page = 100 series)
        api_url = "https://api.themoviedb.org/3/tv/popular"
        params = {
            'api_key': settings.TMDB_API_KEY,
            'language': 'en-US',
            'page': page,
        }
        response = requests.get(api_url, params=params)
        if response.status_code == 200:
            popular_series = response.json().get('results', [])
            for series in popular_series:
                # Avoid duplicates by using get_or_create
                Series.objects.get_or_create(
                    id=series['id'],
                    defaults={
                        'title': series.get('name', 'Unknown Title'),
                        'description': series.get('overview', 'No description available.'),
                        'release_date': series.get('first_air_date', 'Unknown Date'),
                        'genre': 'Unknown',  # TMDB does not provide genres directly for series
                        'rating': series.get('vote_average', 0),
                        'poster_path': series.get('poster_path', ''),
                    },
                )
        else:
            print(f"Failed to fetch page {page}. Status code: {response.status_code}")
