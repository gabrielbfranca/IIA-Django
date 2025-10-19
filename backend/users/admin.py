from django.contrib import admin
from .models import User, ArtworkLike, UserRecommendationHistory


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        "username",
        "email",
        "first_name",
        "last_name",
        "get_liked_count",
        "date_joined",
    ]
    search_fields = ["username", "email", "first_name", "last_name"]
    list_filter = ["date_joined", "is_active", "is_staff"]
    readonly_fields = ["date_joined", "last_login"]


@admin.register(ArtworkLike)
class ArtworkLikeAdmin(admin.ModelAdmin):
    list_display = ["user", "artwork_id", "liked_at"]
    list_filter = ["liked_at"]
    search_fields = ["user__username", "artwork_id"]


@admin.register(UserRecommendationHistory)
class UserRecommendationHistoryAdmin(admin.ModelAdmin):
    list_display = ["user", "source_artwork_id", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["user__username", "source_artwork_id"]
