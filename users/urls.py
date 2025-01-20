from django.urls import path
from users import views

urlpatterns = [
    path('registration/', views.register_api_view),
    path('authorization/', views.authorize_api_view),
    path('SMSCode/', views.sms_code_api_view)
]