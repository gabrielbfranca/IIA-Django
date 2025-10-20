import os
import json
import pickle
import numpy as np
import pandas as pd
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
        self.utility_matrix = None
        self._load_model()

    def _load_model(self):
        """Load pre-trained model files"""
        try:
            print(f"Django BASE_DIR: {settings.BASE_DIR}")
            print(f"Django BASE_DIR.parent: {settings.BASE_DIR.parent}")

            # Look for models in the models directory (relative to project root)
            # Direct path construction since we know the structure
            # BASE_DIR points to backend/, we need to go to parent for project root

            # More robust path detection
            current_file_dir = os.path.dirname(os.path.abspath(__file__))
            
            project_root = os.path.dirname(os.path.dirname(current_file_dir))
            models_path = os.path.join(project_root, "models")

            print(f"Looking for models in: {models_path}")  # Debug log

            # Check if models directory exists
            if os.path.exists(models_path):
                print(f" Models directory exists")
                print(f"Files in models directory: {os.listdir(models_path)}")
            else:
                print(f" Models directory does not exist: {models_path}")
                raise FileNotFoundError(f"Models directory not found: {models_path}")

            # Load vectorizer
            vectorizer_path = os.path.join(models_path, "vectorizer.pkl")
            print(f"Loading vectorizer from: {vectorizer_path}")
            with open(vectorizer_path, "rb") as f:
                self.vectorizer = pickle.load(f)

            # Load TF-IDF matrix
            matrix_path = os.path.join(models_path, "tfidf_matrix.npz")
            self.tfidf_matrix = load_npz(matrix_path)

            # Load metadata
            metadata_path = os.path.join(models_path, "metadata.json")
            with open(metadata_path, "r") as f:
                self.metadata = json.load(f)

            # Load model info
            model_info_path = os.path.join(models_path, "model_info.json")
            with open(model_info_path, "r") as f:
                self.model_info = json.load(f)

            # Load utility matrix
            utility_path = os.path.join(models_path, "utility_matrix.csv")
            if os.path.exists(utility_path):
                self.utility_matrix = pd.read_csv(utility_path)
            else:
                self.utility_matrix = None

            print(f" Model loaded: {len(self.metadata)} artworks")

        except Exception as e:
            print(f"❌ Error loading model: {e}")
            # Create dummy data for development
            self.metadata = []
            self.model_info = {"n_artworks": 0}
            print("⚠️ Using dummy data - train and save your model first!")

    def get_user_preferences(self, user_id):
        """
        Get user preferences from utility matrix
        Returns list of artwork IDs that the user liked (rating = 1)
        """
        if self.utility_matrix is None:
            return []
        
        # Filter user interactions where rating = 1 (liked)
        user_likes = self.utility_matrix[
            (self.utility_matrix['user_id'] == user_id) & 
            (self.utility_matrix['rating'] == 1)
        ]
        
        return user_likes['artwork_id'].tolist()

    def get_recommendations(self, artwork_id=None, user_id=None, user_likes=None, n_recommendations=10):
        """Get artwork recommendations with optional user personalization"""
        if not self.tfidf_matrix:
            return []

        # SCENARIO 1: Content-based recommendation from specific artwork
        if artwork_id is not None and artwork_id < len(self.metadata):
            # Calculate base similarity
            similarity_scores = cosine_similarity(
                self.tfidf_matrix[artwork_id : artwork_id + 1], self.tfidf_matrix
            ).flatten()

            # Apply user personalization if user_id provided
            if user_id is not None and self.utility_matrix is not None:
                user_preferences = self.get_user_preferences(user_id)
                print(f"🎯 Personalizing for user {user_id} with {len(user_preferences)} liked artworks")
                
                # Boost similarity scores based on user's liked artworks
                for liked_id in user_preferences:
                    if 0 <= liked_id < len(similarity_scores):
                        liked_similarity = cosine_similarity(
                            self.tfidf_matrix[liked_id : liked_id + 1], self.tfidf_matrix
                        ).flatten()
                        similarity_scores += 0.3 * liked_similarity

            # Apply manual user_likes boost (for backward compatibility)
            if user_likes:
                for liked_id in user_likes:
                    if 0 <= liked_id < len(similarity_scores):
                        liked_similarity = cosine_similarity(
                            self.tfidf_matrix[liked_id : liked_id + 1], self.tfidf_matrix
                        ).flatten()
                        similarity_scores += 0.3 * liked_similarity

        # SCENARIO 2: User-based recommendation (no specific artwork)
        elif user_id is not None and self.utility_matrix is not None:
            user_preferences = self.get_user_preferences(user_id)
            print(f"🔍 Generating recommendations based on user {user_id} profile")
            
            if not user_preferences:
                print("⚠️ User has no preferences - using random recommendations")
                similarity_scores = np.random.rand(len(self.metadata))
            else:
                # Calculate average similarity to user's liked artworks
                similarity_scores = np.zeros(len(self.metadata))
                for liked_id in user_preferences:
                    if 0 <= liked_id < len(self.metadata):
                        liked_similarity = cosine_similarity(
                            self.tfidf_matrix[liked_id : liked_id + 1], self.tfidf_matrix
                        ).flatten()
                        similarity_scores += liked_similarity
                
                similarity_scores /= len(user_preferences)  # Average
                
                # Penalize already rated items
                user_interactions = self.utility_matrix[
                    self.utility_matrix['user_id'] == user_id
                ]['artwork_id'].tolist()
                
                for rated_id in user_interactions:
                    if 0 <= rated_id < len(similarity_scores):
                        similarity_scores[rated_id] *= 0.1  # Heavy penalty

        else:
            # SCENARIO 3: No personalization - random or error
            print("⚠️ No artwork_id or user_id provided")
            return []

        # Get top recommendations
        similar_indices = similarity_scores.argsort()[::-1]
        recommendations = []

        for idx in similar_indices:
            if (artwork_id is None or idx != artwork_id) and len(recommendations) < n_recommendations:
                artwork_info = self.metadata[idx].copy()
                artwork_info["similarity_score"] = float(similarity_scores[idx])
                
                # Add user rating info if available
                if user_id is not None and self.utility_matrix is not None:
                    user_rating = self.utility_matrix[
                        (self.utility_matrix['user_id'] == user_id) & 
                        (self.utility_matrix['artwork_id'] == idx)
                    ]
                    artwork_info['user_rating'] = user_rating['rating'].iloc[0] if len(user_rating) > 0 else None
                
                recommendations.append(artwork_info)

        return recommendations

    def get_artwork_by_id(self, artwork_id):
        """Get artwork metadata by ID"""
        if 0 <= artwork_id < len(self.metadata):
            return self.metadata[artwork_id]
        return None

    def get_model_stats(self):
        """Get model statistics"""
        return self.model_info if self.model_info else {"n_artworks": 0}


# Create singleton instance
recommender_instance = None


def get_recommender():
    """Get or create recommender instance"""
    global recommender_instance
    if recommender_instance is None:
        recommender_instance = ArtworkRecommender()
    return recommender_instance
