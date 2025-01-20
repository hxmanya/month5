from rest_framework import serializers
from .models import Director, Movie, Review

class DirectorItemSerializer(serializers.Serializer):
    class Meta:
        model = Director
        fields = '__all__'


class DirectorSerializer(serializers.ModelSerializer):
    movies_count = serializers.SerializerMethodField()

    class Meta:
        model = Director
        fields = ["id", "name", "movies_count"]

    def get_movies_count(self, obj):
        return obj.movies.count()


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class MovieSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    class Meta:
        model = Movie
        fields = [
            "id",
            "title",
            "description",
            "duration",
            "director",
            "reviews",
            "average_rating",
        ]

    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews:
            total_rating = sum([review.stars for review in reviews])
            return total_rating / len(reviews)
        return 0