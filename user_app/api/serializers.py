from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from django.db import models


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        username = models.CharField(max_length=20, validators=[UniqueValidator(queryset=User.objects.all())])
        extra_kwargs = {
            'password': {'write_only': True}
        }

        
        
        
    def create(self, validated_data):
        
        password = validated_data['password']
        password2 = validated_data['password2']
        
        if password != password2:
            raise serializers.ValidationError({'Password and password2 should be the same'})
        
        
        if User.objects.filter(username=validated_data['username']).exists():
            raise serializers.ValidationError({'error': 'account with this username already exists'})
        
        
        account = User(email=validated_data['email'], username=validated_data['username'])
        account = User(email=validated_data['email'], username="henry")
        account.set_password(password)
        account.save()
        
        return account