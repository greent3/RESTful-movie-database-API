from django.urls import path
from movielist_app.api import views


urlpatterns = [
    path('list/', views.MovieList.as_view(), name='movie-list'),
    path('<int:pk>/', views.MovieById.as_view(), name='movie-detail'),
        
    path('stream/list/', views.StreamPlatformList.as_view(), name='stream-list' ),
    path('stream/<int:pk>/', views.StreamPlatformById.as_view(), name='stream-detail' ),
    
    path('<int:pk>/review/', views.ReviewList.as_view(), name='reviews-for-movie'),
    path('review/<int:pk>/', views.ReviewById.as_view(), name='review-detail'),
        
    path('<int:pk>/review-create/', views.ReviewCreate.as_view(), name='review-create'),
    path('reviews/<str:username>/', views.ReviewsByUser.as_view(), name='reviews-by-user')
]
