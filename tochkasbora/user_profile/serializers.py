from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db import models
from rest_framework import serializers

from user_profile.models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {
            'id': {
                'read_only': True
            },
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.pop('password'))
        return User.objects.create(**validated_data)

    def update(self, instance: models.Model, validated_data: dict):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if 'password' in validated_data:
            instance.password = make_password(validated_data['password'])

        instance.save()

        return instance


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            'user_id',
            'first_name',
            'last_name',
            'email',
            'about',
            'birthday',
            'avatar_path',
            'rate',
            'sex',
            'is_organizer'
        )
        extra_kwargs = {
            'rate': {
                'read_only': True
            },
            'is_organizer': {
                'read_only': True
            }
        }
