"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from api.views import (
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
