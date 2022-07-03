from django.urls import include, path
from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("", include("django.contrib.auth.urls")),
]
