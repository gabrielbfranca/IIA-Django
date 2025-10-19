from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator


class User(AbstractUser):
    """Extended user model with profile information"""

    bio = models.TextField(blank=True, max_length=500)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    def get_liked_artworks(self):
        """Get list of artwork IDs this user has liked"""
        return list(self.artwork_likes.values_list("artwork_id", flat=True))

    def get_liked_count(self):
        """Get total number of artworks liked by user"""
        return self.artwork_likes.count()


class ArtworkLike(models.Model):
    """Model to track user likes for artworks"""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="artwork_likes"
    )
    artwork_id = models.IntegerField(validators=[MinValueValidator(0)])
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user", "artwork_id"]
        ordering = ["-liked_at"]

    def __str__(self):
        return f"{self.user.username} likes artwork {self.artwork_id}"


class UserRecommendationHistory(models.Model):
    """Track recommendation history for analytics"""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="recommendation_history"
    )
    source_artwork_id = models.IntegerField(validators=[MinValueValidator(0)])
    recommended_artwork_ids = models.JSONField()  # List of recommended artwork IDs
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Recommendations for {self.user.username} from artwork {self.source_artwork_id}"
