from django.urls import path
from movie_app import views


urlpatterns = [
    path('', views.directors_list_api_view),
    path('<int:id>/', views.director_detail_api_view),
    path('movies/', views.movies_list_api_view),
    path('movies/<int:id>/', views.movie_detail_api_view),
    path('reviews/', views.reviews_list_api_view),
    path('reviews/<int:id>/', views.review_detail_api_view),
]