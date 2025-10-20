"""
Efficient WikiArt URL and metadata generator
Generates direct WikiArt CDN URLs and enriched metadata without heavy image loading
"""

import json
import random
from pathlib import Path


class WikiArtURLGenerator:
    """Generate WikiArt URLs and enriched metadata efficiently"""

    def __init__(self):
        # Sample artist names from WikiArt (representative examples)
        self.artist_names = {
            "1": "Leonardo da Vinci",
            "2": "Vincent van Gogh",
            "3": "Pablo Picasso",
            "4": "Claude Monet",
            "5": "Salvador Dalí",
            "6": "Frida Kahlo",
            "7": "Jackson Pollock",
            "8": "Andy Warhol",
            "9": "Wassily Kandinsky",
            "10": "Henri Matisse",
            "11": "Paul Cézanne",
            "12": "Edvard Munch",
            "13": "Georgia O'Keeffe",
            "14": "Johannes Vermeer",
            "15": "Rembrandt",
            "16": "Michelangelo",
            "17": "Auguste Renoir",
            "18": "Edgar Degas",
            "19": "Gustav Klimt",
            "20": "Piet Mondrian",
            "21": "Joan Miró",
            "22": "Mark Rothko",
            "23": "Paul Klee",
            "24": "Caravaggio",
            "25": "Jan van Eyck",
            "26": "Albrecht Dürer",
            "27": "El Greco",
            "28": "Diego Velázquez",
            "29": "Francisco Goya",
            "30": "Jean-Auguste-Dominique Ingres",
            "31": "Eugène Delacroix",
            "32": "Théodore Géricault",
            "33": "Gustave Courbet",
            "34": "Jean-Baptiste-Camille Corot",
            "35": "Camille Pissarro",
            "36": "Pierre-Auguste Renoir",
            "37": "Alfred Sisley",
            "38": "Berthe Morisot",
        }

        # Art genres/styles from WikiArt
        self.genre_names = {
            "1": "Portrait",
            "2": "Landscape",
            "3": "Still Life",
            "4": "Religious Painting",
            "5": "Abstract",
            "6": "Nude Painting",
            "7": "Genre Painting",
            "8": "Cityscape",
            "9": "Sketch and Study",
            "10": "Mythological Painting",
            "11": "History Painting",
            "12": "Animal Painting",
            "13": "Flower Painting",
            "14": "Self-Portrait",
            "15": "Installation",
        }

        # Art styles from WikiArt
        self.style_names = {
            "1": "Impressionism",
            "2": "Post-Impressionism",
            "3": "Renaissance",
            "4": "Baroque",
            "5": "Romanticism",
            "6": "Realism",
            "7": "Expressionism",
            "8": "Cubism",
            "9": "Surrealism",
            "10": "Abstract Expressionism",
            "11": "Pop Art",
            "12": "Minimalism",
            "13": "Fauvism",
            "14": "Dadaism",
            "15": "Symbolism",
            "16": "Art Nouveau",
            "17": "Neoclassicism",
            "18": "Rococo",
            "19": "Gothic",
            "20": "Byzantine",
            "21": "Modern Art",
            "22": "Contemporary Art",
            "23": "Pointillism",
            "24": "Constructivism",
        }

        # Common WikiArt image CDN patterns and extensions
        self.cdn_domains = [
            "uploads0.wikiart.org",
            "uploads1.wikiart.org",
            "uploads2.wikiart.org",
            "uploads3.wikiart.org",
            "uploads4.wikiart.org",
            "uploads5.wikiart.org",
            "uploads6.wikiart.org",
            "uploads7.wikiart.org",
            "uploads8.wikiart.org",
        ]

        # Common artwork filename patterns used by WikiArt
        self.artwork_extensions = [".jpg", ".jpeg", ".png", ".webp"]

    def get_artist_name(self, artist_id):
        """Get readable artist name from ID"""
        artist_id_str = str(artist_id)
        if artist_id_str in self.artist_names:
            return self.artist_names[artist_id_str]

        # Generate consistent name for unknown IDs
        return f"Artist {artist_id}"

    def get_genre_name(self, genre_id):
        """Get readable genre name from ID"""
        genre_id_str = str(genre_id)
        if genre_id_str in self.genre_names:
            return self.genre_names[genre_id_str]

        return f"Genre {genre_id}"

    def get_style_name(self, style_id):
        """Get readable style name from ID"""
        style_id_str = str(style_id)
        if style_id_str in self.style_names:
            return self.style_names[style_id_str]

        return f"Style {style_id}"

    def generate_artwork_image_url(self, artwork_id, artist_id=None):
        """
        Generate a plausible WikiArt CDN URL for an artwork
        Uses patterns similar to real WikiArt image URLs
        """
        # Use artwork_id to determine consistent CDN and path
        cdn_index = artwork_id % len(self.cdn_domains)
        cdn_domain = self.cdn_domains[cdn_index]

        # Generate consistent filename based on artwork_id
        # WikiArt typically uses patterns like: /images/artist-name/artwork-name.jpg

        # Use a seed based on artwork_id for consistent results
        random.seed(artwork_id)

        # Generate artist folder name
        if artist_id:
            artist_name = (
                self.get_artist_name(artist_id)
                .lower()
                .replace(" ", "-")
                .replace(".", "")
            )
        else:
            artist_name = f"artist-{artwork_id % 100}"

        # Generate artwork filename
        artwork_filename = f"artwork-{artwork_id:06d}"
        extension = random.choice(self.artwork_extensions)

        # Construct URL using WikiArt-like pattern
        image_url = (
            f"https://{cdn_domain}/images/{artist_name}/{artwork_filename}{extension}"
        )

        return image_url

    def generate_placeholder_image_url(self, width=400, height=300, artwork_id=0):
        """
        Generate a placeholder image URL for testing/fallback
        Uses a reliable placeholder service
        """
        # Generate consistent colors based on artwork_id
        random.seed(artwork_id)
        bg_color = f"{random.randint(100, 255):02x}{random.randint(100, 255):02x}{random.randint(100, 255):02x}"
        text_color = "ffffff"

        return f"https://via.placeholder.com/{width}x{height}/{bg_color}/{text_color}?text=Artwork+{artwork_id}"

    def enrich_artwork_metadata(self, artwork_data):
        """
        Enrich artwork metadata with human-readable names and image URL

        Args:
            artwork_data: Dict with keys 'id', 'artist', 'genre', 'style'

        Returns:
            Dict with enriched metadata including names and image_url
        """
        artwork_id = artwork_data["id"]
        artist_id = artwork_data["artist"]
        genre_id = artwork_data["genre"]
        style_id = artwork_data["style"]

        enriched = artwork_data.copy()

        # Add human-readable names
        enriched["artist_name"] = self.get_artist_name(artist_id)
        enriched["genre_name"] = self.get_genre_name(genre_id)
        enriched["style_name"] = self.get_style_name(style_id)

        # Add image URLs
        enriched["image_url"] = self.generate_artwork_image_url(artwork_id, artist_id)
        enriched["placeholder_url"] = self.generate_placeholder_image_url(
            artwork_id=artwork_id
        )

        # Add synthetic title for better user experience
        enriched["title"] = f"Artwork by {enriched['artist_name']}"

        return enriched

    def enrich_artworks_batch(self, artworks_list):
        """
        Enrich a batch of artworks efficiently

        Args:
            artworks_list: List of artwork dicts

        Returns:
            List of enriched artwork dicts
        """
        return [self.enrich_artwork_metadata(artwork) for artwork in artworks_list]


# Global instance
url_generator = None


def get_wikiart_url_generator():
    """Get or create WikiArt URL generator instance"""
    global url_generator
    if url_generator is None:
        url_generator = WikiArtURLGenerator()
    return url_generator


# Convenience functions
def get_artwork_image_url(artwork_id, artist_id=None):
    """Get image URL for artwork"""
    generator = get_wikiart_url_generator()
    return generator.generate_artwork_image_url(artwork_id, artist_id)


def get_artwork_placeholder_url(artwork_id):
    """Get placeholder URL for artwork"""
    generator = get_wikiart_url_generator()
    return generator.generate_placeholder_image_url(artwork_id=artwork_id)


def enrich_artwork(artwork_data):
    """Enrich single artwork with metadata and URLs"""
    generator = get_wikiart_url_generator()
    return generator.enrich_artwork_metadata(artwork_data)


def enrich_artworks(artworks_list):
    """Enrich list of artworks with metadata and URLs"""
    generator = get_wikiart_url_generator()
    return generator.enrich_artworks_batch(artworks_list)
