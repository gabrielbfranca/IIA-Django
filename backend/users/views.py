from rest_framework import status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import login

from .models import User, ArtworkLike, UserRecommendationHistory
from .serializers import (
    UserRegistrationSerializer,
    UserProfileSerializer,
    UserLoginSerializer,
    ArtworkLikeSerializer,
)


class UserRegistrationView(APIView):
    """User registration endpoint"""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response(
                {
                    "user": UserProfileSerializer(user).data,
                    "token": token.key,
                    "message": "User created successfully",
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    """User login endpoint"""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response(
                {
                    "user": UserProfileSerializer(user).data,
                    "token": token.key,
                    "message": "Login successful",
                }
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileViewSet(ModelViewSet):
    """User profile management"""

    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    @action(detail=False, methods=["get"])
    def me(self, request):
        """Get current user profile"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=["post"])
    def like_artwork(self, request):
        """Like an artwork"""
        artwork_id = request.data.get("artwork_id")
        if not artwork_id:
            return Response(
                {"error": "artwork_id is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        like, created = ArtworkLike.objects.get_or_create(
            user=request.user, artwork_id=int(artwork_id)
        )

        if created:
            return Response(
                {"message": "Artwork liked", "like": ArtworkLikeSerializer(like).data},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {
                    "message": "Artwork already liked",
                    "like": ArtworkLikeSerializer(like).data,
                }
            )

    @action(detail=False, methods=["delete"])
    def unlike_artwork(self, request):
        """Unlike an artwork"""
        artwork_id = request.data.get("artwork_id")
        if not artwork_id:
            return Response(
                {"error": "artwork_id is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            like = ArtworkLike.objects.get(
                user=request.user, artwork_id=int(artwork_id)
            )
            like.delete()
            return Response({"message": "Artwork unliked"})
        except ArtworkLike.DoesNotExist:
            return Response(
                {"error": "Like not found"}, status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=["get"])
    def liked_artworks(self, request):
        """Get user's liked artworks"""
        likes = ArtworkLike.objects.filter(user=request.user).order_by("-liked_at")
        return Response(
            {
                "likes": ArtworkLikeSerializer(likes, many=True).data,
                "count": likes.count(),
            }
        )
