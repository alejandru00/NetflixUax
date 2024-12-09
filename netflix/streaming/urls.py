from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),  # Home view
    path('playlist/', views.playlist, name='playlist'),  # Playlist view
    path('movie/<int:movie_id>/', views.movie_details_page, name='movie-details'),
    path('search/', views.search_movies, name='search-movies'),

    # Series URLs
    path('series/', views.series_page, name='series'),
    path('series/<int:series_id>/', views.series_details_page, name='series-details'),
    path('search-series/', views.search_series, name='search-series'),

    # Add to playlist
    path('add-to-playlist/<int:content_id>/<str:content_type>/', views.add_to_playlist, name='add-to-playlist'),


    # Inicio sesión
    path('login/', auth_views.LoginView.as_view(template_name='streaming/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]
