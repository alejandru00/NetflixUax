from django.urls import path
from .views import signup, login_view, logout_view
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView



urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='authentication/login.html'), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
]
