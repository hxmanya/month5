from django.contrib import admin
from django.urls import path, include
from . import swagger

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/directors/', include('movie_app.urls')),
    path('api/v1/movies/', include('movie_app.urls')),
    path('api/v1/reviews/', include('movie_app.urls')),
    path('api/v1/users/', include('users.urls')),
]
urlpatterns += swagger.urlpatterns
