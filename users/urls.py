from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig

from . import views

app_name = UsersConfig.name

urlpatterns = [
    path("register/", views.UserCreateView.as_view(), name="register"),
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page="users:login"), name="logout"),
    path("<int:pk>/", views.UserRetrieveView.as_view(), name="user-detail"),
    path("<int:pk>/update/", views.UserUpdateView.as_view(), name="user-update"),
]
