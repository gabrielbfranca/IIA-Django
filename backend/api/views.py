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
            user_likes = request.data.get("user_likes", [])
            n_recommendations = request.data.get("n_recommendations", 10)

            if artwork_id is None:
                return Response(
                    {"error": "artwork_id is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Get recommendations
            recommendations = recommender.get_recommendations(
                artwork_id=int(artwork_id),
                user_likes=user_likes,
                n_recommendations=n_recommendations,
            )

            # Enhance recommendations with real WikiArt data
            enhanced_recommendations = wikiart_client.enrich_artworks_batch(
                recommendations
            )

            # Enhance source artwork
            source_artwork = recommender.get_artwork_by_id(int(artwork_id))
            enhanced_source = (
                wikiart_client.enrich_artwork_metadata(source_artwork)
                if source_artwork
                else None
            )

            return Response(
                {
                    "source_artwork": enhanced_source,
                    "recommendations": enhanced_recommendations,
                    "count": len(recommendations),
                }
            )

        except Exception as e:
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
