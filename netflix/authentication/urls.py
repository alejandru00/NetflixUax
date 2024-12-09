from django.urls import path
from .views import signup, CustomLoginView

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("login/", CustomLoginView.as_view(), name="login"),
]
