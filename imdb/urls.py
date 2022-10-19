from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('imdb/', include('movielist_app.api.urls')),
    path('account/', include('user_app.api.urls')),
]
