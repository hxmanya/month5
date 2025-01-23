from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.core.mail import send_mail
import random

from .serializers import UserRegisterSerializer, UserAuthSerializer, SMSCodeSerializer
from .models import SMScode


class RegisterAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")
        username = serializer.validated_data.get("username")
        password = serializer.validated_data.get("password")
        is_active = False

        user = User.objects.create_user(
            username=username, password=password, email=email, is_active=is_active
        )
        code = "".join([str(random.randint(0, 9)) for _ in range(6)])
        SMScode.objects.create(user=user, code=code)
        send_mail(
            "Your code",
            message=code,
            from_email="<EMAIL>",
            recipient_list=[user.email],
        )
        return Response(data={"user_id": user.id}, status=status.HTTP_201_CREATED)


class AuthorizeAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]
        user = authenticate(username=username, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response(data={"key": token.key}, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_401_UNAUTHORIZED)


class SMSCodeAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = SMSCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        sms_code = serializer.validated_data["sms_code"]
        try:
            sms = SMScode.objects.get(code=sms_code)
        except SMScode.DoesNotExist:
            return Response({"error": "Invalid code"}, status=status.HTTP_400_BAD_REQUEST)

        sms.user.is_active = True
        sms.user.save()
        sms.delete()
        return Response(status=status.HTTP_200_OK)