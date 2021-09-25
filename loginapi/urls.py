from .views import ProfileAPI, RegisterAPI, LoginAPI
from django.urls import path
from knox import views as knox_views

urlpatterns = [
    path("register", RegisterAPI.as_view(), name="register"),
    path("login", LoginAPI.as_view(), name="login"),
    path("logout", knox_views.LogoutView.as_view(), name="logout"),
    path("profile", ProfileAPI.as_view(), name="profile"),
]
