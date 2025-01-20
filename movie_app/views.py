from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Director, Movie, Review
from .serializers import (DirectorSerializer, MovieSerializer, ReviewSerializer, DirectorItemSerializer,
                          DirectorValidateSerializers, MovieValidateSerializers, ReviewValidateSerializers)
from rest_framework import status


@api_view(["GET", "PUT", "DELETE"])
def director_detail_api_view(request, id):
    try:
        director = Director.objects.get(id=id)
    except Director.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        data = DirectorSerializer(director).data
        return Response(data=data)
    elif request.method == "PUT":
        serializer = DirectorValidateSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        director.name = serializer.validated_data.get("name")
        director.save()
        return Response(data=DirectorItemSerializer(director).data, status=status.HTTP_201_CREATED)
    elif request.method == "DELETE":
        director.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
def directors_list_api_view(request):
    if request.method == "GET":
        directors = Director.objects.all()
        list_ = DirectorSerializer(instance=directors, many=True).data
        return Response(data=list_)
    elif request.method == "POST":
        serializer = DirectorValidateSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        director = Director.objects.create(name=serializer.validated_data.get('name'))
        return Response(data=DirectorItemSerializer(director).data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "DELETE"])
def movie_detail_api_view(request, id):
    try:
        movie = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        data = MovieSerializer(movie).data
        return Response(data=data)
    elif request.method == "PUT":
        serializer = MovieValidateSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        movie.title = serializer.validated_data.get("title")
        movie.description = serializer.validated_data.get("description")
        movie.duration = serializer.validated_data.get("duration")
        movie.director_id = serializer.validated_data.get("director")
        movie.save()
        return Response(data=MovieSerializer(movie).data, status=status.HTTP_201_CREATED)
    elif request.method == "DELETE":
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
def movies_list_api_view(request):
    if request.method == "GET":
        movies = Movie.objects.all()
        list_ = MovieSerializer(instance=movies, many=True).data
        return Response(data=list_)
    elif request.method == "POST":
        serializer = MovieValidateSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)

        movie = Movie.objects.create(
            title=serializer.validated_data.get("title"),
            description=serializer.validated_data.get("description"),
            duration=serializer.validated_data.get("duration"),
            director_id=serializer.validated_data.get("director")
        )

        return Response(data=MovieSerializer(movie).data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "DELETE"])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        data = ReviewSerializer(review).data
        return Response(data=data)
    elif request.method == "PUT":
        serializer = ReviewValidateSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        review.text = serializer.validated_data.get("text")
        review.stars = serializer.validated_data.get("stars")
        review.movie_id = serializer.validated_data.get("movie")
        review.save()
        return Response(data=ReviewSerializer(review).data, status=status.HTTP_201_CREATED)
    elif request.method == "DELETE":
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
def reviews_list_api_view(request):
    if request.method == "GET":
        reviews = Review.objects.all()
        list_ = ReviewSerializer(instance=reviews, many=True).data
        return Response(data=list_)
    elif request.method == "POST":
        serializer = ReviewValidateSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)

        review = Review.objects.create(
            text=serializer.validated_data.get("text"),
            stars=serializer.validated_data.get("stars"),
            movie_id=serializer.validated_data.get("movie")
        )

        return Response(data=ReviewSerializer(review).data, status=status.HTTP_201_CREATED)