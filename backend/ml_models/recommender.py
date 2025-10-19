import os
import json
import pickle
import numpy as np
from scipy.sparse import load_npz
from sklearn.metrics.pairwise import cosine_similarity
from django.conf import settings


class ArtworkRecommender:
    """Django ML Recommendation System"""

    def __init__(self):
        self.vectorizer = None
        self.tfidf_matrix = None
        self.metadata = None
        self.model_info = None
        self._load_model()

    def _load_model(self):
        """Load pre-trained model files"""
        try:
            # Model files path
            models_path = os.path.join(settings.BASE_DIR.parent, "saved_models")

            # Load vectorizer
            with open(f"{models_path}/vectorizer.pkl", "rb") as f:
                self.vectorizer = pickle.load(f)

            # Load TF-IDF matrix
            self.tfidf_matrix = load_npz(f"{models_path}/tfidf_matrix.npz")

            # Load metadata
            with open(f"{models_path}/metadata.json", "r") as f:
                self.metadata = json.load(f)

            # Load model info
            with open(f"{models_path}/model_info.json", "r") as f:
                self.model_info = json.load(f)

            print(f"✅ Model loaded: {len(self.metadata)} artworks")

        except Exception as e:
            print(f"❌ Error loading model: {e}")
            raise

    def get_recommendations(self, artwork_id, user_likes=None, n_recommendations=10):
        """Get artwork recommendations"""
        if not self.tfidf_matrix or artwork_id >= len(self.metadata):
            return []

        # Calculate base similarity
        similarity_scores = cosine_similarity(
            self.tfidf_matrix[artwork_id : artwork_id + 1], self.tfidf_matrix
        ).flatten()

        # Apply user likes boost
        if user_likes:
            for liked_id in user_likes:
                if 0 <= liked_id < len(similarity_scores):
                    liked_similarity = cosine_similarity(
                        self.tfidf_matrix[liked_id : liked_id + 1], self.tfidf_matrix
                    ).flatten()
                    similarity_scores += 0.3 * liked_similarity

        # Get top recommendations
        similar_indices = similarity_scores.argsort()[::-1]
        recommendations = []

        for idx in similar_indices:
            if idx != artwork_id and len(recommendations) < n_recommendations:
                artwork_info = self.metadata[idx].copy()
                artwork_info["similarity_score"] = float(similarity_scores[idx])
                recommendations.append(artwork_info)

        return recommendations

    def get_artwork_by_id(self, artwork_id):
        """Get artwork metadata by ID"""
        if 0 <= artwork_id < len(self.metadata):
            return self.metadata[artwork_id]
        return None

    def get_model_stats(self):
        """Get model statistics"""
        return self.model_info


# Create singleton instance
recommender_instance = None


def get_recommender():
    """Get or create recommender instance"""
    global recommender_instance
    if recommender_instance is None:
        recommender_instance = ArtworkRecommender()
    return recommender_instance
