/**
 * API Service for communicating with the backend.
 * 
 * Following Single Responsibility Principle:
 * - Handles all HTTP communication with the backend API
 */

import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

/**
 * Axios instance with default configuration
 */
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

/**
 * News API Service
 */
class NewsApiService {
  /**
   * Fetch all news articles
   * @returns {Promise<Array>} Array of news articles
   */
  async getTodayNews() {
    try {
      const response = await apiClient.get('/news/');
      return response.data.results || [];
    } catch (error) {
      console.error('Error fetching news:', error);
      throw this._handleError(error);
    }
  }

  /**
   * Refresh news from RSS feed (fetches all articles)
   * @returns {Promise<Object>} Response with updated articles
   */
  async refreshNews() {
    try {
      const response = await apiClient.post('/news/refresh/?all=1');
      return response.data;
    } catch (error) {
      console.error('Error refreshing news:', error);
      throw this._handleError(error);
    }
  }

  /**
   * Get all news articles with pagination
   * @param {number} page - Page number
   * @returns {Promise<Object>} Paginated response
   */
  async getAllNews(page = 1) {
    try {
      const response = await apiClient.get(`/news/?page=${page}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching all news:', error);
      throw this._handleError(error);
    }
  }

  /**
   * Handle API errors
   * @private
   */
  _handleError(error) {
    if (error.response) {
      // Server responded with error status
      return new Error(error.response.data.error || 'Server error occurred');
    } else if (error.request) {
      // Request made but no response
      return new Error('Network error: Unable to reach server');
    } else {
      // Something else happened
      return new Error(error.message || 'An unexpected error occurred');
    }
  }
}

const newsApiInstance = new NewsApiService();
export default newsApiInstance;
