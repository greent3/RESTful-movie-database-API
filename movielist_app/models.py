from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

class StreamPlatform(models.Model):
    platform = models.CharField(max_length=30, unique=True)
    about = models.CharField(max_length=50)
    website = models.URLField(max_length=100)
    
    def __str__(self):
        return self.platform

class Movie(models.Model):
    title = models.CharField(max_length=50)
    storyline = models.CharField(max_length=200)
    platform = models.ForeignKey(StreamPlatform, on_delete=models.CASCADE, related_name="watchlist", default=None)
    active = models.BooleanField(default=True)
    avg_rating = models.FloatField(default=0)
    num_ratings = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ['title', 'storyline', 'platform']
    
    def __str__(self):
        return self.title

class Review(models.Model):
    review_user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveBigIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.CharField(max_length=200)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="reviews")
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "Score: " + str(self.rating) + " | " + self.watchlist.title + " | " + str(self.review_user)