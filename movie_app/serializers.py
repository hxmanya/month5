from rest_framework import serializers
from .models import Director, Movie, Review


class DirectorItemSerializer(serializers.ModelSerializer):
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

class DirectorValidateSerializers(serializers.Serializer):
    name = serializers.CharField(required=True, min_length=3, max_length=100)

    def validate_name(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("Имя должно содержать только буквы.")
        return value


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


class MovieValidateSerializers(serializers.Serializer):
    title = serializers.CharField(required=True, max_length=255)
    description = serializers.CharField(required=True)
    duration = serializers.IntegerField(min_value=1)
    director = serializers.IntegerField(required=True)

    def validate_director(self, value):
        try:
            Director.objects.get(id=value)
        except Director.DoesNotExist:
            raise serializers.ValidationError("Указанный режиссер не существует.")
        return value

class ReviewValidateSerializers(serializers.Serializer):
    text = serializers.CharField(required=True, max_length=1000)
    stars = serializers.IntegerField(required=True, min_value=1, max_value=5)
    movie = serializers.IntegerField(required=True)

    def validate_movie(self, value):
        try:
            Movie.objects.get(id=value)
        except Movie.DoesNotExist:
            raise serializers.ValidationError("Указанный фильм не существует.")
        return value