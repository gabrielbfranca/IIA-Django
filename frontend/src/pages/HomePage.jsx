import React, { useState, useEffect } from "react";
import apiService from "../services/api";
import { useAuth } from "../contexts/AuthContext";
import ArtworkModal from "../components/ArtworkModal";
import "./HomePage.css";

const HomePage = () => {
  const { user, logout } = useAuth();
  const [artworks, setArtworks] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [likedArtworks, setLikedArtworks] = useState(new Set());
  const [selectedArtwork, setSelectedArtwork] = useState(null);
  const [modalArtwork, setModalArtwork] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  // Load initial data
  useEffect(() => {
    const loadData = async () => {
      try {
        setLoading(true);
        // Get artworks (images now come as URLs, much faster)
        const response = await apiService.getArtworks(currentPage, 12, false);
        setArtworks(response.artworks);
        setTotalPages(Math.ceil(response.total / 12));
      } catch (err) {
        setError("Failed to load artworks");
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, [currentPage]);

  useEffect(() => {
    loadLikedArtworks();
  }, []);

  const loadLikedArtworks = async () => {
    try {
      const response = await apiService.getLikedArtworks();
      const likedIds = new Set(response.likes.map((like) => like.artwork_id));
      setLikedArtworks(likedIds);
    } catch (err) {
      console.error("Failed to load liked artworks:", err);
    }
  };

  const handleLikeArtwork = async (artworkId) => {
    try {
      if (likedArtworks.has(artworkId)) {
        await apiService.unlikeArtwork(artworkId);
        setLikedArtworks((prev) => {
          const newSet = new Set(prev);
          newSet.delete(artworkId);
          return newSet;
        });
      } else {
        await apiService.likeArtwork(artworkId);
        setLikedArtworks((prev) => new Set([...prev, artworkId]));
      }

      // Update recommendations if we have a selected artwork
      if (selectedArtwork) {
        await loadRecommendations(selectedArtwork.id);
      }
    } catch (err) {
      console.error("Failed to toggle like:", err);
      alert("Failed to update like status");
    }
  };

  const loadRecommendations = async (artworkId) => {
    try {
      const userLikes = Array.from(likedArtworks);
      const response = await apiService.getRecommendations(
        artworkId,
        userLikes,
        8
      );
      setRecommendations(response.recommendations);
      setSelectedArtwork(response.source_artwork);
    } catch (err) {
      console.error("Failed to load recommendations:", err);
      setError("Failed to load recommendations");
    }
  };

  // Helper function to get image URL from artwork data
  const getArtworkImageUrl = (artwork) => {
    // Use the new efficient URL structure from backend
    if (artwork.image_url) {
      return artwork.image_url;
    }
    // Fallback to placeholder
    return (
      artwork.placeholder_url ||
      `https://via.placeholder.com/400x300/4A5568/FFFFFF?text=Artwork+${artwork.id}`
    );
  };

  const handleArtworkClick = (artwork) => {
    setSelectedArtwork(artwork);
    loadRecommendations(artwork.id);
  };

  const handleArtworkModalOpen = (artwork) => {
    setModalArtwork(artwork);
    setIsModalOpen(true);
  };

  const handleModalClose = () => {
    setIsModalOpen(false);
    setModalArtwork(null);
  };

  if (loading && artworks.length === 0) {
    return <div className="center">Loading artworks...</div>;
  }

  return (
    <div className="home-page">
      {/* Header */}
      <header className="app-header">
        <div className="header-content">
          <h1>Art Recommendation App</h1>
          <div className="user-info">
            <span>Welcome, {user?.username}!</span>
            <button onClick={logout} className="logout-btn">
              Logout
            </button>
          </div>
        </div>
      </header>

      <div className="main-content">
        {/* Artwork Gallery */}
        <section className="artwork-gallery">
          <h2>Artwork Gallery</h2>
          {error && <div className="error-message">{error}</div>}

          <div className="artworks-grid">
            {artworks.map((artwork) => (
              <div
                key={artwork.id}
                className={`artwork-card ${
                  selectedArtwork?.id === artwork.id ? "selected" : ""
                }`}
              >
                <div
                  className="artwork-image-container"
                  onClick={() => handleArtworkModalOpen(artwork)}
                >
                  <img
                    src={getArtworkImageUrl(artwork)}
                    alt={`Artwork ${artwork.id}`}
                    className="artwork-image"
                    onError={(e) => {
                      e.target.src =
                        artwork.placeholder_url ||
                        `https://via.placeholder.com/400x300/4A5568/FFFFFF?text=Artwork+${artwork.id}`;
                    }}
                  />
                  <div className="image-overlay">
                    <span>View Details</span>
                  </div>
                </div>

                <div
                  className="artwork-info"
                  onClick={() => handleArtworkClick(artwork)}
                >
                  <h3>{artwork.title || `Artwork #${artwork.id}`}</h3>
                  <p>
                    <strong>Artist:</strong>{" "}
                    {artwork.artist_name || `Artist ${artwork.artist}`}
                  </p>
                  <p>
                    <strong>Style:</strong>{" "}
                    {artwork.style_name || `Style ${artwork.style}`}
                  </p>
                  <p>
                    <strong>Genre:</strong>{" "}
                    {artwork.genre_name || `Genre ${artwork.genre}`}
                  </p>
                </div>

                <button
                  className={`like-btn ${
                    likedArtworks.has(artwork.id) ? "liked" : ""
                  }`}
                  onClick={(e) => {
                    e.stopPropagation();
                    handleLikeArtwork(artwork.id);
                  }}
                >
                  {likedArtworks.has(artwork.id) ? "❤️" : "🤍"}
                </button>
              </div>
            ))}
          </div>

          {/* Pagination */}
          <div className="pagination">
            <button
              onClick={() => setCurrentPage((prev) => Math.max(1, prev - 1))}
              disabled={currentPage === 1}
            >
              Previous
            </button>
            <span>
              Page {currentPage} of {totalPages}
            </span>
            <button
              onClick={() =>
                setCurrentPage((prev) => Math.min(totalPages, prev + 1))
              }
              disabled={currentPage === totalPages}
            >
              Next
            </button>
          </div>
        </section>

        {/* Recommendations */}
        {selectedArtwork && (
          <section className="recommendations">
            <h2>
              Recommendations based on "
              {selectedArtwork.title || `Artwork ${selectedArtwork.id}`}"
            </h2>
            <p className="rec-subtitle">
              {likedArtworks.size > 0
                ? `Personalized for your ${likedArtworks.size} liked artworks`
                : "Like some artworks to get personalized recommendations!"}
            </p>

            <div className="recommendations-grid">
              {recommendations.map((artwork) => (
                <div key={artwork.id} className="recommendation-card">
                  <div
                    className="rec-artwork-image-container"
                    onClick={() => handleArtworkModalOpen(artwork)}
                  >
                    <img
                      src={getArtworkImageUrl(artwork)}
                      alt={`Artwork ${artwork.id}`}
                      className="rec-artwork-image"
                      onError={(e) => {
                        e.target.src =
                          artwork.placeholder_url ||
                          `https://via.placeholder.com/200x150/4A5568/FFFFFF?text=Art+${artwork.id}`;
                      }}
                    />
                  </div>

                  <div className="artwork-info">
                    <h4>{artwork.title || `Artwork #${artwork.id}`}</h4>
                    <p>
                      <strong>Artist:</strong>{" "}
                      {artwork.artist_name || `Artist ${artwork.artist}`}
                    </p>
                    <p>
                      <strong>Style:</strong>{" "}
                      {artwork.style_name || `Style ${artwork.style}`}
                    </p>
                    <p className="similarity">
                      Similarity: {(artwork.similarity_score * 100).toFixed(1)}%
                    </p>
                  </div>

                  <button
                    className={`like-btn ${
                      likedArtworks.has(artwork.id) ? "liked" : ""
                    }`}
                    onClick={() => handleLikeArtwork(artwork.id)}
                  >
                    {likedArtworks.has(artwork.id) ? "❤️" : "🤍"}
                  </button>
                </div>
              ))}
            </div>
          </section>
        )}

        {/* User Stats */}
        <section className="user-stats">
          <h3>Your Stats</h3>
          <div className="stats-grid">
            <div className="stat-card">
              <span className="stat-number">{likedArtworks.size}</span>
              <span className="stat-label">Liked Artworks</span>
            </div>
            <div className="stat-card">
              <span className="stat-number">{recommendations.length}</span>
              <span className="stat-label">Current Recommendations</span>
            </div>
          </div>
        </section>
      </div>

      {/* Artwork Modal */}
      <ArtworkModal
        artwork={modalArtwork}
        isOpen={isModalOpen}
        onClose={handleModalClose}
        onLike={handleLikeArtwork}
        isLiked={modalArtwork ? likedArtworks.has(modalArtwork.id) : false}
      />
    </div>
  );
};

export default HomePage;
