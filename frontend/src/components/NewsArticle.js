/**
 * NewsArticle Component
 * 
 * Displays a single news article with title, link, and publication date
 */

import React from 'react';
import './NewsArticle.css';

const NewsArticle = ({ article }) => {
  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <article className="news-article">
      <div className="article-content">
        <h2 className="article-title">
          <a
            href={article.link}
            target="_blank"
            rel="noopener noreferrer"
            className="article-link"
          >
            {article.title}
          </a>
        </h2>
        {article.description && (
          <p className="article-description">{article.description}</p>
        )}
        <div className="article-meta">
          <span className="article-source">{article.source}</span>
          <span className="article-separator">•</span>
          <time className="article-date" dateTime={article.published_date}>
            {formatDate(article.published_date)}
          </time>
        </div>
      </div>
      <div className="article-arrow">→</div>
    </article>
  );
};

export default NewsArticle;
