from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.http import JsonResponse
from backend.ml_models.model_loader import get_recommender
from backend.ml_models.wikiart_api_client import get_wikiart_client


class ArtworkListView(APIView):
    """List artworks with pagination"""

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        try:
            recommender = get_recommender()
            wikiart_client = get_wikiart_client()

            # Get pagination parameters
            page = int(request.GET.get("page", 1))
            page_size = int(request.GET.get("page_size", 20))

            # Calculate pagination
            start_idx = (page - 1) * page_size
            end_idx = start_idx + page_size

            # Get artworks slice from recommender metadata
            base_artworks = recommender.metadata[start_idx:end_idx]

            # Enhance with real WikiArt data and URLs
            enhanced_artworks = wikiart_client.enrich_artworks_batch(base_artworks)

            return Response(
                {
                    "artworks": enhanced_artworks,
                    "page": page,
                    "page_size": page_size,
                    "total": len(recommender.metadata),
                    "has_next": end_idx < len(recommender.metadata),
                }
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ArtworkDetailView(APIView):
    """Get artwork details by ID"""

    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        try:
            recommender = get_recommender()
            wikiart_client = get_wikiart_client()

            artwork = recommender.get_artwork_by_id(pk)

            if not artwork:
                return Response(
                    {"error": "Artwork not found"}, status=status.HTTP_404_NOT_FOUND
                )

            # Enhance with real WikiArt data
            enhanced_artwork = wikiart_client.enrich_artwork_metadata(artwork)

            return Response({"artwork": enhanced_artwork})

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class RecommendationView(APIView):
    """Get recommendations for an artwork"""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            recommender = get_recommender()
            wikiart_client = get_wikiart_client()

            # Get request data
            artwork_id = request.data.get("artwork_id")
            user_id = request.data.get("user_id")  # Optional user ID
            user_likes = request.data.get("user_likes", [])
            n_recommendations = request.data.get("n_recommendations", 10)

            # Validate inputs - now supports both artwork_id and user_id scenarios
            if artwork_id is None and user_id is None:
                return Response(
                    {"error": "Either artwork_id or user_id is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Get recommendations with enhanced utility matrix support
            recommendations = recommender.get_recommendations(
                artwork_id=int(artwork_id) if artwork_id is not None else None,
                user_id=int(user_id) if user_id is not None else None,
                user_likes=user_likes,
                n_recommendations=n_recommendations
            )

            if not recommendations:
                return Response(
                    {
                        "message": "No recommendations found",
                        "artwork_id": artwork_id,
                        "user_id": user_id,
                        "recommendations": [],
                        "count": 0,
                    }
                )

            # Enhance recommendations with real WikiArt data
            enhanced_recommendations = wikiart_client.enrich_artworks_batch(
                recommendations
            )

            # Prepare response
            response_data = {
                "recommendations": enhanced_recommendations,
                "count": len(recommendations),
            }

            # Add source artwork if artwork_id was provided
            if artwork_id is not None:
                source_artwork = recommender.get_artwork_by_id(int(artwork_id))
                enhanced_source = (
                    wikiart_client.enrich_artwork_metadata(source_artwork)
                    if source_artwork
                    else None
                )
                response_data["source_artwork"] = enhanced_source
                response_data["artwork_id"] = artwork_id

            # Add user context
            if user_id is not None:
                response_data["user_id"] = user_id
                # Get user preferences for debugging
                user_preferences = recommender.get_user_preferences(int(user_id))
                response_data["user_preferences_count"] = len(user_preferences)

            return Response(response_data)

        except Exception as e:
            print(f"🚨 RecommendationView Error: {e}")
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ArtworkImageView(APIView):
    """Get artwork image URLs by ID"""

    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        try:
            wikiart_client = get_wikiart_client()

            # Generate real WikiArt image URLs
            image_url = wikiart_client.generate_wikiart_image_url(pk)
            placeholder_url = wikiart_client.generate_placeholder_url(artwork_id=pk)

            return Response(
                {
                    "artwork_id": pk,
                    "image_url": image_url,
                    "placeholder_url": placeholder_url,
                }
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ModelStatsView(APIView):
    """Get ML model statistics"""

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        try:
            recommender = get_recommender()
            stats = recommender.get_model_stats()

            return Response({"model_stats": stats})

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
