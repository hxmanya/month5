from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import UserRegisterSerializer, UserAuthSerializer, SMSCodeSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
import random
from .models import SMScode
from django.core.mail import send_mail


@api_view(["POST"])
def register_api_view(request):
    serializer = UserRegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    email = serializer.validated_data.get("email")
    username = serializer.validated_data.get("username")
    password = serializer.validated_data.get("password")
    is_active = False
    user = User.objects.create_user(
        username=username, password=password, email=email, is_active=is_active
    )
    code = "".join([str(random.randint(0, 9)) for i in range(6)])
    SMScode.objects.create(user=user, code=code)
    send_mail(
        "Your code",
        message=code,
        from_email="<EMAIL>",
        recipient_list=[user.email],
    )
    return Response(data={"user_id": user.id}, status=status.HTTP_201_CREATED)


@api_view(["POST"])
def authorize_api_view(request):
    serializer = UserAuthSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data["username"]
    password = serializer.validated_data["password"]
    user = authenticate(username=username, password=password)
    if user is not None:
        try:
            token = Token.objects.get(user=user)
        except:
            token = Token.objects.create(user=user)
        return Response(data={"key": token.key})
    return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(["POST"])
def sms_code_api_view(request):
    serializer = SMSCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    sms_code = serializer.validated_data["sms_code"]
    try:
        sms = SMScode.objects.get(code=sms_code)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    sms.user.is_active = True
    sms.user.save()
    sms.delete()
    return Response(status=status.HTTP_200_OK)