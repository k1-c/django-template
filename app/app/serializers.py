from rest_framework import serializers
from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('user', 'username', 'parent', 'birthday', 'phone_number')


class UserProfileDetailSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = UserProfile
        fields = ('email', 'username', 'affiliate_id', 'parent_id', 'birthday', 'phone_number')
