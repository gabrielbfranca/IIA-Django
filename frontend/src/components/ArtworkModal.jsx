import React from "react";
import "./ArtworkModal.css";

const ArtworkModal = ({ artwork, isOpen, onClose, onLike, isLiked }) => {
  if (!isOpen || !artwork) return null;

  // Helper function to get image URL from artwork data
  const getArtworkImageUrl = (artwork) => {
    // Use the new efficient URL structure from backend
    if (artwork.image_url) {
      return artwork.image_url;
    }
    // Fallback to placeholder
    return (
      artwork.placeholder_url ||
      `https://via.placeholder.com/800x600/4A5568/FFFFFF?text=Artwork+${artwork.id}`
    );
  };

  const handleOverlayClick = (e) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  return (
    <div className="modal-overlay" onClick={handleOverlayClick}>
      <div className="modal-content">
        <button className="modal-close" onClick={onClose}>
          ×
        </button>

        <div className="modal-body">
          <div className="modal-image-section">
            <img
              src={getArtworkImageUrl(artwork)}
              alt={`Artwork ${artwork.id}`}
              className="modal-artwork-image"
              onError={(e) => {
                e.target.src =
                  artwork.placeholder_url ||
                  `https://via.placeholder.com/800x600/4A5568/FFFFFF?text=Artwork+${artwork.id}`;
              }}
            />
          </div>

          <div className="modal-info-section">
            <div className="modal-header">
              <h2>{artwork.title || `Artwork #${artwork.id}`}</h2>
              <button
                className={`modal-like-btn ${isLiked ? "liked" : ""}`}
                onClick={() => onLike(artwork.id)}
                title={isLiked ? "Unlike this artwork" : "Like this artwork"}
              >
                {isLiked ? "❤️ Liked" : "🤍 Like"}
              </button>
            </div>

            <div className="artwork-details">
              <div className="detail-item">
                <span className="detail-label">Artist:</span>
                <span className="detail-value">
                  {artwork.artist_name || `Artist ${artwork.artist}`}
                </span>
              </div>

              <div className="detail-item">
                <span className="detail-label">Style:</span>
                <span className="detail-value">
                  {artwork.style_name || `Style ${artwork.style}`}
                </span>
              </div>

              <div className="detail-item">
                <span className="detail-label">Genre:</span>
                <span className="detail-value">
                  {artwork.genre_name || `Genre ${artwork.genre}`}
                </span>
              </div>

              <div className="detail-item">
                <span className="detail-label">Artwork ID:</span>
                <span className="detail-value">{artwork.id}</span>
              </div>

              {artwork.similarity_score && (
                <div className="detail-item">
                  <span className="detail-label">Similarity:</span>
                  <span className="detail-value similarity-score">
                    {(artwork.similarity_score * 100).toFixed(1)}%
                  </span>
                </div>
              )}
            </div>

            <div className="modal-actions">
              <button className="btn-secondary" onClick={onClose}>
                Close
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ArtworkModal;
