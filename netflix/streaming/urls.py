from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Página principal
    path('playlist/', views.playlist, name='playlist'),  # Playlist
    path('movie/<int:movie_id>/', views.movie_details_page, name='movie-details'),  # Detalles de película
    path('search/', views.search_movies, name='search-movies'),  # Búsqueda de películas

    # Series URLs
    path('series/', views.series_page, name='series'),  # Página de series
    path('series/<int:series_id>/', views.series_details_page, name='series-details'),  # Detalles de serie
    path('search-series/', views.search_series, name='search-series'),  # Búsqueda de series

    # Añadir a playlist
    path('add-to-playlist/<int:content_id>/<str:content_type>/', views.add_to_playlist, name='add-to-playlist')
]
