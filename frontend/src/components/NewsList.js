/**
 * NewsList Component
 * 
 * Displays a list of news articles with loading and error states
 */

import React from 'react';
import NewsArticle from './NewsArticle';
import './NewsList.css';

const NewsList = ({ articles, loading, error }) => {
  if (loading) {
    return (
      <div className="news-list-container">
        <div className="loading-spinner">
          <div className="spinner"></div>
          <p>Loading today's sports news...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="news-list-container">
        <div className="error-message">
          <span className="error-icon">⚠️</span>
          <h3>Oops! Something went wrong</h3>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  if (articles.length === 0) {
    return (
      <div className="news-list-container">
        <div className="empty-state">
          <span className="empty-icon">📰</span>
          <h3>No articles found</h3>
          <p>There are no sports news articles published today yet.</p>
          <p className="empty-hint">Try refreshing to fetch the latest news.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="news-list-container">
      <div className="news-count">
        {articles.length} {articles.length === 1 ? 'article' : 'articles'} found
      </div>
      <div className="news-list">
        {articles.map((article) => (
          <NewsArticle key={article.id} article={article} />
        ))}
      </div>
    </div>
  );
};

export default NewsList;
