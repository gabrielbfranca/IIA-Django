from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from ..ml_models.recommender import get_recommender


class ArtworkListView(APIView):
    """List artworks with pagination"""

    def get(self, request):
        try:
            recommender = get_recommender()

            # Get pagination parameters
            page = int(request.GET.get("page", 1))
            page_size = int(request.GET.get("page_size", 20))

            # Calculate pagination
            start_idx = (page - 1) * page_size
            end_idx = start_idx + page_size

            # Get artworks slice
            artworks = recommender.metadata[start_idx:end_idx]

            return Response(
                {
                    "artworks": artworks,
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

    def get(self, request, pk):
        try:
            recommender = get_recommender()
            artwork = recommender.get_artwork_by_id(pk)

            if not artwork:
                return Response(
                    {"error": "Artwork not found"}, status=status.HTTP_404_NOT_FOUND
                )

            return Response({"artwork": artwork})

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class RecommendationView(APIView):
    """Get recommendations for an artwork"""

    def post(self, request):
        try:
            recommender = get_recommender()

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

            return Response(
                {
                    "source_artwork": recommender.get_artwork_by_id(int(artwork_id)),
                    "recommendations": recommendations,
                    "count": len(recommendations),
                }
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ModelStatsView(APIView):
    """Get ML model statistics"""

    def get(self, request):
        try:
            recommender = get_recommender()
            stats = recommender.get_model_stats()

            return Response({"model_stats": stats})

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
