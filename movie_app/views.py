from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from collections import OrderedDict
from .models import Director, Movie, Review
from .serializers import (
    DirectorSerializer,
    MovieSerializer,
    ReviewSerializer,
    DirectorItemSerializer,
    DirectorValidateSerializers,
    MovieValidateSerializers,
    ReviewValidateSerializers,
)


class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response(
            OrderedDict(
                [
                    ("total", self.page.paginator.count),
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("results", data),
                ]
            )
        )


class DirectorListCreateAPIView(ListCreateAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    pagination_class = CustomPagination

    def create(self, request, *args, **kwargs):
        serializer = DirectorValidateSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        director = Director.objects.create(name=serializer.validated_data.get("name"))
        return Response(
            data=DirectorItemSerializer(director).data, status=status.HTTP_201_CREATED
        )


class DirectorDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    lookup_field = "id"

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = DirectorValidateSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance.name = serializer.validated_data.get("name")
        instance.save()
        return Response(
            data=DirectorItemSerializer(instance).data, status=status.HTTP_201_CREATED
        )


class MovieListCreateAPIView(ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    pagination_class = CustomPagination

    def create(self, request, *args, **kwargs):
        serializer = MovieValidateSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        movie = Movie.objects.create(
            title=serializer.validated_data.get("title"),
            description=serializer.validated_data.get("description"),
            duration=serializer.validated_data.get("duration"),
            director_id=serializer.validated_data.get("director"),
        )
        return Response(
            data=MovieSerializer(movie).data, status=status.HTTP_201_CREATED
        )


class MovieDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    lookup_field = "id"

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = MovieValidateSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance.title = serializer.validated_data.get("title")
        instance.description = serializer.validated_data.get("description")
        instance.duration = serializer.validated_data.get("duration")
        instance.director_id = serializer.validated_data.get("director")
        instance.save()
        return Response(
            data=MovieSerializer(instance).data, status=status.HTTP_201_CREATED
        )


class ReviewListCreateAPIView(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = CustomPagination

    def create(self, request, *args, **kwargs):
        serializer = ReviewValidateSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        review = Review.objects.create(
            text=serializer.validated_data.get("text"),
            stars=serializer.validated_data.get("stars"),
            movie_id=serializer.validated_data.get("movie"),
        )
        return Response(
            data=ReviewSerializer(review).data, status=status.HTTP_201_CREATED
        )


class ReviewDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_field = "id"

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ReviewValidateSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance.text = serializer.validated_data.get("text")
        instance.stars = serializer.validated_data.get("stars")
        instance.movie_id = serializer.validated_data.get("movie")
        instance.save()
        return Response(
            data=ReviewSerializer(instance).data, status=status.HTTP_201_CREATED
        )