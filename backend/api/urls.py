from django.urls import path
from .views import (
    ArtworkListView,
    ArtworkDetailView,
    RecommendationView,
    ModelStatsView,
)

urlpatterns = [
    path("artworks/", ArtworkListView.as_view(), name="artwork-list"),
    path("artworks/<int:pk>/", ArtworkDetailView.as_view(), name="artwork-detail"),
    path("recommendations/", RecommendationView.as_view(), name="recommendations"),
    path("model-stats/", ModelStatsView.as_view(), name="model-stats"),
]
