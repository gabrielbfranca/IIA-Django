#!/usr/bin/env python3
"""
Test script for WikiArt API client
"""

from ml_models.wikiart_api_client import get_wikiart_client
import json


def test_wikiart_client():
    """Test the WikiArt API client functionality"""

    print("🎨 Testing WikiArt API Client")
    print("=" * 50)

    # Test the WikiArt client
    client = get_wikiart_client()

    # Test with some sample artwork data
    test_artwork = {
        "id": 100,
        "artist": "2",  # Pablo Picasso
        "genre": "1",  # Portrait
        "style": "8",  # Cubism
        "likes": 0,
    }

    print(f"Original artwork data:")
    print(json.dumps(test_artwork, indent=2))
    print()

    # Enrich the artwork
    enriched = client.enrich_artwork_metadata(test_artwork)

    print(f"Enriched artwork data:")
    print(json.dumps(enriched, indent=2))
    print()

    print("🖼️ Generated URLs:")
    print(f"  Primary Image: {enriched['image_url']}")
    print(f"  Placeholder: {enriched['placeholder_url']}")
    print(f"  WikiArt Page: {enriched['wikiart_page']}")
    print()

    print("📋 Extracted Metadata:")
    print(f"  Title: {enriched['title']}")
    print(f"  Artist: {enriched['artist_name']}")
    print(f"  Genre: {enriched['genre_name']}")
    print(f"  Style: {enriched['style_name']}")
    print()

    # Test with a batch of artworks
    test_batch = [
        {
            "id": 1,
            "artist": "1",
            "genre": "2",
            "style": "1",
            "likes": 0,
        },  # Van Gogh, Landscape, Impressionism
        {
            "id": 2,
            "artist": "3",
            "genre": "1",
            "style": "3",
            "likes": 0,
        },  # Da Vinci, Portrait, Renaissance
        {
            "id": 3,
            "artist": "5",
            "genre": "5",
            "style": "9",
            "likes": 0,
        },  # Dalí, Abstract, Surrealism
    ]

    print("🎨 Testing batch processing:")
    enriched_batch = client.enrich_artworks_batch(test_batch)

    for i, artwork in enumerate(enriched_batch):
        print(f"  {i+1}. {artwork['title']} by {artwork['artist_name']}")
        print(f"     Style: {artwork['style_name']}, Genre: {artwork['genre_name']}")
        print(f"     Image: {artwork['image_url']}")
        print()

    print("✅ WikiArt API integration working successfully!")
    return enriched


if __name__ == "__main__":
    test_wikiart_client()
