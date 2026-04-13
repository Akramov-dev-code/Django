from django.urls import path

from . import views

urlpatterns = [
    path("", views.index_view, name="index"),
    path("about/", views.about_developer, name="about"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path('course/<int:pk>/', views.course_detail, name='course_detail'),
    path('course/<int:pk>/checkout/', views.checkout, name='checkout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/delete/<int:pk>/', views.delete_student, name='delete_student'),
    path('dashboard/add/', views.add_student, name='add_student'),
    path('dashboard/edit/<int:pk>/', views.edit_student, name='edit_student'),
    path('logout/', views.logout_view, name='logout'),
]