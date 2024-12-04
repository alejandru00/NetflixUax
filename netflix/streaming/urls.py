from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home view
    path('playlist/', views.playlist, name='playlist'),  # Playlist view
    path('movie/<int:movie_id>/', views.movie_details_page, name='movie-details'),
    path('search/', views.search_movies, name='search-movies'),
    path('add-to-playlist/<int:movie_id>/', views.add_to_playlist, name='add-to-playlist'),

    # Series URLs
    path('series/', views.series_page, name='series'),
    path('series/<int:series_id>/', views.series_details_page, name='series-details'),
    path('search-series/', views.search_series, name='search-series'),
    path('add-to-series-playlist/<int:series_id>/', views.add_to_series_playlist, name='add-to-series-playlist'),
]
