from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, ArtworkLike, UserRecommendationHistory


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""

    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "password_confirm",
            "first_name",
            "last_name",
            "bio",
            "location",
            "birth_date",
        ]

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError("Passwords don't match")
        return attrs

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        password = validated_data.pop("password")
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile"""

    liked_count = serializers.ReadOnlyField(source="get_liked_count")
    liked_artworks = serializers.ReadOnlyField(source="get_liked_artworks")

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "location",
            "birth_date",
            "avatar",
            "liked_count",
            "liked_artworks",
            "date_joined",
        ]
        read_only_fields = ["id", "username", "date_joined"]


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login"""

    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError("Invalid credentials")
            if not user.is_active:
                raise serializers.ValidationError("User account is disabled")
            attrs["user"] = user
            return attrs
        else:
            raise serializers.ValidationError("Must include username and password")


class ArtworkLikeSerializer(serializers.ModelSerializer):
    """Serializer for artwork likes"""

    class Meta:
        model = ArtworkLike
        fields = ["id", "artwork_id", "liked_at"]
        read_only_fields = ["id", "liked_at"]


class UserRecommendationHistorySerializer(serializers.ModelSerializer):
    """Serializer for recommendation history"""

    class Meta:
        model = UserRecommendationHistory
        fields = ["id", "source_artwork_id", "recommended_artwork_ids", "created_at"]
        read_only_fields = ["id", "created_at"]
