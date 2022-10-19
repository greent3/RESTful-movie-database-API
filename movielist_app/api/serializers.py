from rest_framework import serializers
from movielist_app import models 

class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = models.Review
        exclude = ['movie']

class MovieSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True) 
    platform = serializers.CharField(source="platform.platform")
    
    class Meta:
        model = models.Movie
        fields = "__all__"
        
    # field validator
    def validate_title(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Movie title must be at least 2 characters")
        return value
    
    # object validator
    def validate(self, data):
        if data['title'] == data['storyline']:
            raise serializers.ValidationError("Movie title must be different from movie storyline")
        return data

class StreamPlatformSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(many=True, read_only=True)
    
    class Meta:
        model = models.StreamPlatform
        fields = "__all__"

        