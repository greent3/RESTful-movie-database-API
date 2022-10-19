from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, filters
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from movielist_app import models
from movielist_app.api.pagination import MovieListPagination
from movielist_app.api import permissions, serializers, throttling


class ReviewsByUser(generics.ListAPIView):    
    serializer_class = serializers.ReviewSerializer
    permission_classes = [IsAdminUser]
    
    def get_queryset(self):
        queryset = models.Review.objects.get_queryset().order_by('id')
        username = self.request.query_params.get('username')
        if username is not None:
            queryset = queryset.filter(review_user__username=username)
        return queryset



class ReviewCreate(generics.CreateAPIView):
    serializer_class = serializers.ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [throttling.ReviewCreateThrottle]
    
    def get_queryset(self):
        return models.Review.objects.get_queryset().order_by('id')
    
    
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        movie = models.Movie.objects.get(pk=pk)
        review_user = self.request.user
        review_queryset = models.Review.objects.filter(movie=movie, review_user = review_user)
        
        if review_queryset.exists():
            raise ValidationError("You have already reviewed this movie")
               
        if movie.num_ratings == 0:
            movie.avg_rating = serializer.validated_data['rating']
        else:
             movie.avg_rating = ((movie.avg_rating + serializer.validated_data['rating']) / 2)
        
        movie.num_ratings = movie.num_ratings + 1
        movie.save()
        serializer.save(movie=movie, review_user=review_user)




class ReviewList(generics.ListAPIView):
    filter_backends = [DjangoFilterBackend]
    serializer_class = serializers.ReviewSerializer
    filterset_fields = ['review_user__username', 'active']
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        return models.Review.objects.order_by('created').filter(movie=pk) 




    
class ReviewById(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.ReviewUserOrReadOnly]
    queryset = models.Review.objects.get_queryset().order_by('id')
    serializer_class = serializers.ReviewSerializer  

    
    
class StreamPlatformById(APIView):
    permission_classes = [permissions.IsAdminOrReadOnly]
    
    def get(self, request, pk):
        try:
            platform = models.StreamPlatform.objects.get(pk=pk)
        except models.StreamPlatform.DoesNotExist:
            return Response({'error': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.StreamPlatformSerializer(platform)
        return Response(serializer.data)
    
    def put(self, request, pk):
        platform = models.StreamPlatform.objects.get(pk=pk)
        serializer = serializers.StreamPlatformSerializer(platform, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    
    def delete(self, request, pk):
        platform = models.StreamPlatform.objects.get(pk=pk)
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




class StreamPlatformList(APIView):
    permission_classes = [permissions.IsAdminOrReadOnly]
    
    def get(self, request):
        platform = models.StreamPlatform.objects.get_queryset().order_by('id')
        serializer = serializers.StreamPlatformSerializer(platform, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = serializers.StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    


class MovieList(generics.ListAPIView):
    queryset = models.Movie.objects.get_queryset().order_by('id')
    serializer_class = serializers.MovieSerializer
    permission_classes = [permissions.IsAdminOrReadOnly]
    pagination_class = MovieListPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'platform__platform']
    



class MovieById(APIView):
    permission_classes = [permissions.IsAdminOrReadOnly]
    
    def get(self, request, pk):
        try:
            movie = models.Movie.objects.get(pk=pk)
        except models.Movie.DoesNotExist:
            return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.MovieSerializer(movie)
        return Response(serializer.data)
    
    def put(self, request, pk):
        movie = models.Movie.objects.get(pk=pk)
        #serializer = serializers.MovieSerializer(movie, data=request.data)
        serializer = serializers.MovieSerializer(movie, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    
    def delete(self, request, pk):
        movie = models.Movie.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


