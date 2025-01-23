from django.urls import path
from users.views import RegisterAPIView, AuthorizeAPIView, SMSCodeAPIView

urlpatterns = [
    path('registration/', RegisterAPIView.as_view(), name='user-registration'),
    path('authorization/', AuthorizeAPIView.as_view(), name='user-authorization'),
    path('sms-code/', SMSCodeAPIView.as_view(), name='sms-code-verification'),
]