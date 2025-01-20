from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError


class UserBaseSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField()

class UserAuthSerializer(UserBaseSerializer):
    pass

class UserRegisterSerializer(UserBaseSerializer):
    email = serializers.EmailField()
    password_confirm = serializers.CharField(max_length=150)
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise ValidationError('Passwords do not match')
        return data
    def validate_username(self, username):
        try:
            User.objects.get(username=username)
        except:
            return username
        raise ValidationError('Username already exists')

class SMSCodeSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6)