from django.urls import path
from movie_app.views import (
    DirectorListCreateAPIView,
    DirectorDetailAPIView,
    MovieListCreateAPIView,
    MovieDetailAPIView,
    ReviewListCreateAPIView,
    ReviewDetailAPIView,
)

urlpatterns = [
    path('', DirectorListCreateAPIView.as_view(), name='directors-list-create'),
    path('<int:id>/', DirectorDetailAPIView.as_view(), name='director-detail'),
    path('movies/', MovieListCreateAPIView.as_view(), name='movies-list-create'),
    path('movies/<int:id>/', MovieDetailAPIView.as_view(), name='movie-detail'),
    path('reviews/', ReviewListCreateAPIView.as_view(), name='reviews-list-create'),
    path('reviews/<int:id>/', ReviewDetailAPIView.as_view(), name='review-detail'),
]