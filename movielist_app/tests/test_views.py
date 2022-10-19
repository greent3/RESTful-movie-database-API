from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from movielist_app import models


class StreamPlatformTestCase(APITestCase):
    
    def setUp(self):
        self.unauth_user = User.objects.create_user(username="unauth", password="unauth_password")        
        
        self.auth_user = User.objects.create_user(username="auth", password="auth_password")
        self.auth_token = Token.objects.get(user__username=self.auth_user)
        
        self.admin_user = User.objects.create_superuser(username="admin",  password="admin_password")
        self.admin_token = Token.objects.get(user__username=self.admin_user)
        
        self.stream = models.StreamPlatform.objects.create(platform="Netflix", about="#1 Platform", website="https://www.netflix.com")

    
    
    def test_stream_platform_list(self):
        """
        Ensure everyone can view the list of streaming platforms,
            but only admin can create
        """
        
        data = {
            1: {
            "platform": "Hulu",
            "about": "#2 streaming platform",
            "website": "https://www.hulu.com"
            },
            2: {
            "platform": "Prime Video",
            "about": "#3 streaming platform",
            "website": "https://www.prime-video.com"
            }
        }
        # Ensure unauth users are not allowed to create a list of streaming platforms, but can view them
        response = self.client.post(reverse('stream-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.get(reverse('stream-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Ensure auth users are not allowed to create streaming platforms, but can view them
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.auth_token.key)
        response = self.client.post(reverse('stream-list'), format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.get(reverse('stream-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Ensure admin users are allowed to view and create streaming platforms lists       
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        response = self.client.post(reverse('stream-list'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(reverse('stream-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    
    
    
    
        
    def test_stream_platform_ind(self):
        """
        Ensure everyone can view individual steaming platforms
            but only admin can post or delete
        """
        data = {
            "platform": "Updated to Prime Video",
            "about": "#3 streaming platform",
            "website": "https://www.prime-video.com"
            }
        
        # Ensure unauth users can view, but not put or delete
        response = self.client.put(reverse('stream-detail', args=[self.stream.pk]), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        response = self.client.get(reverse('stream-detail', args=[self.stream.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Ensure auth users can view, but not put or delete
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.auth_token.key)
        response = self.client.put(reverse('stream-detail', args=[self.stream.pk]), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        response = self.client.get(reverse('stream-detail', args=[self.stream.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Ensure admin users can view, put, and delete       
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        response = self.client.put(reverse('stream-detail', args=[self.stream.pk]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response = self.client.get(reverse('stream-detail', args=[self.stream.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['platform'], 'Updated to Prime Video')
        
        response = self.client.delete(reverse('stream-detail', args=[self.stream.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
       
    
     
        
        
        
class ReviewTestCase(APITestCase):
    
    def setUp(self):
        self.unauth_user = User.objects.create_user(username="example", password="password@123")        
        
        self.auth_user = User.objects.create_user(username="auth", password="auth_password")
        self.auth_token = Token.objects.get(user__username=self.auth_user)
        
        self.admin_user = User.objects.create_superuser(username="admin",  password="admin_password")
        self.admin_token = Token.objects.get(user__username=self.admin_user)
        
        self.stream = models.StreamPlatform.objects.create(platform="Netflix", 
                                about="#1 Platform", website="https://www.netflix.com")
        self.movie = models.Movie.objects.create(platform=self.stream, title="Chip Skylark",
                                storyline="The life of Chip Skylark", active=True)
        self.movie2 = models.Movie.objects.create(platform=self.stream, title="Avengers Endgame",
                                storyline="The Avengers assemble to take down Thanos", active=True)
        self.review = models.Review.objects.create(review_user=self.admin_user, rating=5, description="Amazing Movie! (Tony Stark dies at the end)", 
                                movie=self.movie2, active=True)
        self.review2 = models.Review.objects.create(review_user=self.auth_user, rating=5, description="Love his shiny teeth!", 
                                movie=self.movie, active=True)
    
    
    
    def test_review_list(self):
        """
        Ensure all users can view a list of reviews for a movie, but not create or delete the list
        """
        
        # ensure unauth user can view only
        response = self.client.get(reverse('reviews-for-movie', args=(self.movie2.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(reverse('reviews-for-movie', args=(self.movie2.id,)))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
        # ensure auth user can view only
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.auth_token.key)
        response = self.client.get(reverse('reviews-for-movie', args=(self.movie2.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(reverse('reviews-for-movie', args=(self.movie2.id,)))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
        # ensure admin user can view only
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        response = self.client.get(reverse('reviews-for-movie', args=(self.movie2.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(reverse('reviews-for-movie', args=(self.movie2.id,)))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)




        
    def test_review_by_id(self):
        """
        Ensure unauth users can view a review, but not delete one
        Ensure auth users can view and also edit if it's their review
        Ensure admin users can view and delete a review
        """
        
        # ensure unauth user can view only
        response = self.client.get(reverse('review-detail', args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(reverse('review-detail', args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # ensure auth user can view only
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.auth_token.key)
        response = self.client.get(reverse('review-detail', args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(reverse('review-detail', args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # ensure user can edit their own review
        review2_updated = {
            "review_user": self.auth_user,
            "rating": 5,
            "description": "Great Movie!",
            "movie": self.movie,
            "active": True
        }
        response = self.client.put(reverse('review-detail', args=(self.review2.id,)), review2_updated)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
        # ensure admin user can view only
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        response = self.client.get(reverse('review-detail', args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(reverse('review-detail', args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)    
        
        
        
    def test_review_create(self):
        """
        Ensure only auth users can create reviews
        Ensure users can't create more than 1 review per movie under the same account
        """
        movie2_review = {
            "review_user": self.auth_user,
            "rating": 5,
            "description": "Great Movie!",
            "movie": self.movie2,
            "active": True
        }

        # ensure unauth users can't create reviews
        response = self.client.post(reverse('review-create', args=(self.movie2.id,)), movie2_review)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # ensure auth users can create reviews
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.auth_token.key)
        response = self.client.post(reverse('review-create', args=(self.movie2.id,)), movie2_review)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Review.objects.count(), 3)
        
        # ensure users can't create multiple reviews for the same movie
        response = self.client.post(reverse('review-create', args=(self.movie2.id,)), movie2_review)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        


    def test_reviews_by_user(self):
        """
        Ensure only admin can view all of a users reviews using their user id
        """
        # ensure unauth users can't access all of a users reviews 
        response = self.client.get(reverse('reviews-by-user', args=(self.auth_user.username,)))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # ensure auth users can't access all of a users reviews
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.auth_token.key)
        response = self.client.get(reverse('reviews-by-user', args=(self.auth_user.username,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # ensure admin users can access all of a users reviews
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        response = self.client.get(reverse('reviews-by-user', args=(self.auth_user.username,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)



        
        
class MovieListTestCase(APITestCase):
    
    def setUp(self):
        self.unauth_user = User.objects.create_user(username="example", password="password@123")        
        
        self.auth_user = User.objects.create_user(username="auth", password="auth_password")
        self.auth_token = Token.objects.get(user__username=self.auth_user)
        
        self.admin_user = User.objects.create_superuser(username="admin",  password="admin_password")
        self.admin_token = Token.objects.get(user__username=self.admin_user)
        
        self.stream = models.StreamPlatform.objects.create(platform="Netflix", about="#1 Platform", website="https://www.netflix.com")
        
        self.movie = models.Movie.objects.create(title="Step Brothers 2", storyline="More Dale and Brennan", platform=self.stream)
        
    def test_movie_list(self):
        """
        Ensure any user can get the list of movies
        Ensure no user can post or delete the list of movies
        """
        movie_list = {
            1: {
                "title": "Larry goes to the beach",
                "storyline": "All about larry's day at the beach",
                "platform": "Netflix"
            },
            2: {
                "title": "Larry doesn't go to the beach",
                "storyline": "All about larry's day away from the beach",
                "platform": "Netflix"
            }
        }
        # ensure unauth users can only get
        response=self.client.get(reverse('movie-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response=self.client.post(reverse('movie-list'), movie_list, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # ensure auth users can only get
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.auth_token.key)
        response=self.client.get(reverse('movie-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response=self.client.post(reverse('movie-list'), movie_list, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # ensure admin users can get, post, and delete movielists
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        response=self.client.get(reverse('movie-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response=self.client.put(reverse('movie-list'), movie_list, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response=self.client.delete(reverse('movie-list'))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
        
    def test_movie_by_id(self):
        """
        Ensure auth and unauth users can only get movies using the movie id
        Ensure admin users can view, update, or delete movies using the movie id
        """
        example_movie = {
            "title": "This is a load of barnacles",
            "storyline": "None",
            "platform": self.stream
            }
        # unauth user
        response=self.client.get(reverse('movie-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response=self.client.post(reverse('movie-detail', args=[2]), example_movie)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # auth user
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.auth_token.key)
        response=self.client.get(reverse('movie-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response=self.client.put(reverse('movie-detail', args=[2]), example_movie)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # auth user
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        response=self.client.get(reverse('movie-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response=self.client.put(reverse('movie-detail', args=[1]), example_movie)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response=self.client.delete(reverse('movie-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
