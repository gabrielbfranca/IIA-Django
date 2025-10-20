const API_BASE_URL = "http://localhost:8000/api";

class ApiService {
  constructor() {
    this.token = localStorage.getItem("token");
  }

  // Helper method to get headers
  getHeaders(includeAuth = true) {
    const headers = {
      "Content-Type": "application/json",
    };

    if (includeAuth && this.token) {
      headers["Authorization"] = `Token ${this.token}`;
    }

    return headers;
  }

  // Handle API responses
  async handleResponse(response) {
    if (!response.ok) {
      let errorMessage = `HTTP ${response.status}`;
      try {
        const errorData = await response.json();

        // Handle Django validation errors
        if (errorData.error) {
          errorMessage = errorData.error;
        } else if (errorData.non_field_errors) {
          errorMessage = errorData.non_field_errors.join(", ");
        } else if (typeof errorData === "object") {
          // Handle field-specific errors
          const fieldErrors = [];
          Object.keys(errorData).forEach((field) => {
            if (Array.isArray(errorData[field])) {
              fieldErrors.push(`${field}: ${errorData[field].join(", ")}`);
            } else {
              fieldErrors.push(`${field}: ${errorData[field]}`);
            }
          });
          if (fieldErrors.length > 0) {
            errorMessage = fieldErrors.join("; ");
          }
        }
      } catch (e) {
        // If response is not JSON, use the status text
        errorMessage = response.statusText || errorMessage;
      }

      throw new Error(errorMessage);
    }
    return response.json();
  }

  // Authentication APIs
  async register(userData) {
    console.log("Sending registration data:", userData); // Debug log

    const response = await fetch(`${API_BASE_URL}/users/register/`, {
      method: "POST",
      headers: this.getHeaders(false),
      body: JSON.stringify(userData),
    });

    console.log("Registration response status:", response.status); // Debug log

    const data = await this.handleResponse(response);
    if (data.token) {
      this.token = data.token;
      localStorage.setItem("token", data.token);
      localStorage.setItem("user", JSON.stringify(data.user));
    }
    return data;
  }

  async login(credentials) {
    const response = await fetch(`${API_BASE_URL}/users/login/`, {
      method: "POST",
      headers: this.getHeaders(false),
      body: JSON.stringify(credentials),
    });

    const data = await this.handleResponse(response);
    if (data.token) {
      this.token = data.token;
      localStorage.setItem("token", data.token);
      localStorage.setItem("user", JSON.stringify(data.user));
    }
    return data;
  }

  logout() {
    this.token = null;
    localStorage.removeItem("token");
    localStorage.removeItem("user");
  }

  // User profile APIs
  async getCurrentUser() {
    const response = await fetch(`${API_BASE_URL}/users/profile/me/`, {
      headers: this.getHeaders(),
    });
    return this.handleResponse(response);
  }

  async likeArtwork(artworkId) {
    const response = await fetch(
      `${API_BASE_URL}/users/profile/like_artwork/`,
      {
        method: "POST",
        headers: this.getHeaders(),
        body: JSON.stringify({ artwork_id: artworkId }),
      }
    );
    return this.handleResponse(response);
  }

  async unlikeArtwork(artworkId) {
    const response = await fetch(
      `${API_BASE_URL}/users/profile/unlike_artwork/`,
      {
        method: "DELETE",
        headers: this.getHeaders(),
        body: JSON.stringify({ artwork_id: artworkId }),
      }
    );
    return this.handleResponse(response);
  }

  async getLikedArtworks() {
    const response = await fetch(
      `${API_BASE_URL}/users/profile/liked_artworks/`,
      {
        headers: this.getHeaders(),
      }
    );
    return this.handleResponse(response);
  }

  // Artwork APIs
  async getArtworks(page = 1, pageSize = 20, includeImages = false) {
    const response = await fetch(
      `${API_BASE_URL}/artworks/?page=${page}&page_size=${pageSize}&include_images=${includeImages}`,
      {
        headers: this.getHeaders(false),
      }
    );
    return this.handleResponse(response);
  }

  async getArtworkDetail(artworkId) {
    const response = await fetch(`${API_BASE_URL}/artworks/${artworkId}/`, {
      headers: this.getHeaders(false),
    });
    return this.handleResponse(response);
  }

  async getArtworkImage(artworkId) {
    const response = await fetch(
      `${API_BASE_URL}/artworks/${artworkId}/image/`,
      {
        headers: this.getHeaders(false),
      }
    );
    return this.handleResponse(response);
  }

  // Recommendation APIs
  async getRecommendations(artworkId, userLikes = [], nRecommendations = 10) {
    const response = await fetch(`${API_BASE_URL}/recommendations/`, {
      method: "POST",
      headers: this.getHeaders(false),
      body: JSON.stringify({
        artwork_id: artworkId,
        user_likes: userLikes,
        n_recommendations: nRecommendations,
      }),
    });
    return this.handleResponse(response);
  }

  async getModelStats() {
    const response = await fetch(`${API_BASE_URL}/model-stats/`, {
      headers: this.getHeaders(false),
    });
    return this.handleResponse(response);
  }
}

const apiService = new ApiService();
export default apiService;
