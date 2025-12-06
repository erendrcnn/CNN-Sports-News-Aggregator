/**
 * Main App Component
 * 
 * Root component that manages application state and coordinates components
 */

import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import NewsList from './components/NewsList';
import newsApi from './services/newsApi';
import './App.css';

function App() {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  /**
   * Fetch today's news articles
   */
  const fetchNews = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await newsApi.getTodayNews();
      setArticles(data);
    } catch (err) {
      setError(err.message);
      console.error('Failed to fetch news:', err);
    } finally {
      setLoading(false);
    }
  };

  /**
   * Refresh news from RSS feed
   */
  const handleRefresh = async () => {
    try {
      setLoading(true);
      setError(null);
      // Trigger refresh on backend
      await newsApi.refreshNews();
      // Then fetch fresh articles from database
      const data = await newsApi.getTodayNews();
      setArticles(data);
    } catch (err) {
      setError(err.message);
      console.error('Failed to refresh news:', err);
    } finally {
      setLoading(false);
    }
  };

  // Fetch news on component mount
  useEffect(() => {
    fetchNews();
  }, []);

  return (
    <div className="app">
      <Header onRefresh={handleRefresh} isLoading={loading} />
      <main className="main-content">
        <NewsList articles={articles} loading={loading} error={error} />
      </main>
      <footer className="footer">
        <p>
          Sports news aggregator powered by{' '}
          <a
            href="http://rss.cnn.com/rss/edition_sport.rss"
            target="_blank"
            rel="noopener noreferrer"
          >
            CNN Sports RSS Feed
          </a>
        </p>
        <p className="footer-tech">
          Built with React, Django, and PostgreSQL
        </p>
      </footer>
    </div>
  );
}

export default App;
