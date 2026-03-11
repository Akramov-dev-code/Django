from django.urls import path

from . import views

urlpatterns = [
    path("", views.index_view, name="index"),
    path("about/", views.about_developer, name="about"),
    path("course/<int:pk>/", views.course_detail, name="course_1detail"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login")
]