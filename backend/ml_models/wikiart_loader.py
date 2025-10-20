from datasets import load_dataset
from django.conf import settings
import os
from PIL import Image
import io
import base64


class WikiArtDatasetLoader:
    """Loader for accessing original WikiArt dataset from Hugging Face"""

    def __init__(self):
        self.dataset = None
        self.dataset_cache = {}
        self.id_mappings = {"artists": {}, "genres": {}, "styles": {}}
        self._load_dataset()
        self._build_mappings()

    def _load_dataset(self):
        """Load the WikiArt dataset from Hugging Face"""
        try:
            print("Loading WikiArt dataset from Hugging Face...")
            self.dataset = load_dataset("huggan/wikiart", streaming=True, split="train")
            print("✅ WikiArt dataset loaded successfully")
        except Exception as e:
            print(f"❌ Error loading WikiArt dataset: {e}")
            self.dataset = None

    def _build_mappings(self):
        """Build mappings from numeric IDs to actual names by sampling dataset"""
        if not self.dataset:
            return

        print("Building ID mappings from dataset sample...")

        # Sample first 1000 items to build mappings
        sample_count = 0
        max_samples = 1000

        for item in self.dataset:
            if sample_count >= max_samples:
                break

            # Store mappings (in real implementation, these would be proper names)
            # For now, we'll create readable labels from the IDs
            artist_id = str(item["artist"])
            genre_id = str(item["genre"])
            style_id = str(item["style"])

            if artist_id not in self.id_mappings["artists"]:
                self.id_mappings["artists"][artist_id] = f"Artist_{artist_id}"

            if genre_id not in self.id_mappings["genres"]:
                self.id_mappings["genres"][genre_id] = f"Genre_{genre_id}"

            if style_id not in self.id_mappings["styles"]:
                self.id_mappings["styles"][style_id] = f"Style_{style_id}"

            # Cache this item for quick access by ID
            self.dataset_cache[sample_count] = {
                "image": item["image"],
                "artist": artist_id,
                "genre": genre_id,
                "style": style_id,
                "artist_name": self.id_mappings["artists"][artist_id],
                "genre_name": self.id_mappings["genres"][genre_id],
                "style_name": self.id_mappings["styles"][style_id],
            }

            sample_count += 1

            if sample_count % 100 == 0:
                print(f"Processed {sample_count} items...")

        print(
            f"✅ Built mappings for {len(self.id_mappings['artists'])} artists, "
            f"{len(self.id_mappings['genres'])} genres, "
            f"{len(self.id_mappings['styles'])} styles"
        )

    def get_artwork_by_id(self, artwork_id):
        """Get artwork data including image by ID"""
        if artwork_id in self.dataset_cache:
            return self.dataset_cache[artwork_id]

        # If not cached, we'd need to iterate through dataset to find it
        # For now, return None for items not in cache
        return None

    def get_image_as_base64(self, artwork_id):
        """Get artwork image as base64 string for web display"""
        artwork = self.get_artwork_by_id(artwork_id)
        if not artwork or "image" not in artwork:
            return None

        try:
            # Convert PIL Image to base64
            image = artwork["image"]
            if hasattr(image, "convert"):
                # Ensure RGB format
                image = image.convert("RGB")

                # Save to bytes buffer
                buffer = io.BytesIO()
                image.save(buffer, format="JPEG", quality=85)
                buffer.seek(0)

                # Convert to base64
                image_data = buffer.getvalue()
                base64_image = base64.b64encode(image_data).decode("utf-8")

                return f"data:image/jpeg;base64,{base64_image}"

        except Exception as e:
            print(f"Error converting image {artwork_id} to base64: {e}")
            return None

    def get_artist_name(self, artist_id):
        """Get readable artist name from ID"""
        return self.id_mappings["artists"].get(str(artist_id), f"Artist_{artist_id}")

    def get_genre_name(self, genre_id):
        """Get readable genre name from ID"""
        return self.id_mappings["genres"].get(str(genre_id), f"Genre_{genre_id}")

    def get_style_name(self, style_id):
        """Get readable style name from ID"""
        return self.id_mappings["styles"].get(str(style_id), f"Style_{style_id}")


# Global instance
wikiart_loader = None


def get_wikiart_loader():
    """Get or create WikiArt dataset loader instance"""
    global wikiart_loader
    if wikiart_loader is None:
        wikiart_loader = WikiArtDatasetLoader()
    return wikiart_loader
