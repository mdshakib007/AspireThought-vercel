from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def save(self):
        username = self.validated_data['username']
        email = self.validated_data['email']
        password = self.validated_data['password']

        if len(password) < 8:
            raise serializers.ValidationError({"error": "Password must be at least 8 characters"})
        
        if get_user_model().objects.filter(email=email).exists():
            raise serializers.ValidationError({'error': "This Email Already Exists!"})

        user = get_user_model().objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return user

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'profile_picture', 'date_of_birth', 'is_verified', 'verification_requested', 'bookmarks', 'library', 'following']


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class BookmarkSerializer(serializers.Serializer):
    slug = serializers.CharField(required=True)

class FollowingSerializer(serializers.Serializer):
    slug = serializers.CharField(required=True)