/**
 * Header Component
 * 
 * Displays the application title and refresh button
 */

import React from 'react';
import './Header.css';

const Header = ({ onRefresh, isLoading }) => {
  return (
    <header className="header">
      <div className="header-content">
        <h1 className="header-title">
          <span className="cnn-logo">CNN</span> Sports News
        </h1>
        <p className="header-subtitle">Today's Headlines</p>
      </div>
      <button
        className="refresh-button"
        onClick={onRefresh}
        disabled={isLoading}
        aria-label="Refresh news"
      >
        {isLoading ? 'Refreshing...' : '🔄 Refresh'}
      </button>
    </header>
  );
};

export default Header;
