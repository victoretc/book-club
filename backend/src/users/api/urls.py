from django.urls import path

from users.api import viewsets


app_name = "users"

urlpatterns = [
    path("me/", viewsets.SelfView.as_view()),
    path("register/", viewsets.RegisterView.as_view(), name="register"),
    path("<int:pk>/books/", viewsets.UserBooksView.as_view(), name="user-books"),
]
