import React from 'react';
import { render, screen } from '@testing-library/react';
import NewsList from './NewsList';

describe('NewsList Component', () => {
  const mockArticles = [
    {
      id: 1,
      title: 'Article 1',
      link: 'https://example.com/1',
      published_date: '2024-01-01T12:00:00Z',
      source: 'CNN Sports',
    },
    {
      id: 2,
      title: 'Article 2',
      link: 'https://example.com/2',
      published_date: '2024-01-01T13:00:00Z',
      source: 'CNN Sports',
    },
  ];

  test('renders loading state', () => {
    render(<NewsList articles={[]} loading={true} error={null} />);
    const loadingText = screen.getByText(/Loading today's sports news/i);
    expect(loadingText).toBeInTheDocument();
  });

  test('renders error state', () => {
    render(
      <NewsList articles={[]} loading={false} error="Failed to fetch news" />
    );
    const errorText = screen.getByText(/Failed to fetch news/i);
    expect(errorText).toBeInTheDocument();
  });

  test('renders empty state', () => {
    render(<NewsList articles={[]} loading={false} error={null} />);
    const emptyText = screen.getByText(/No articles found/i);
    expect(emptyText).toBeInTheDocument();
  });

  test('renders article list', () => {
    render(<NewsList articles={mockArticles} loading={false} error={null} />);
    const article1 = screen.getByText(/Article 1/i);
    const article2 = screen.getByText(/Article 2/i);
    expect(article1).toBeInTheDocument();
    expect(article2).toBeInTheDocument();
  });

  test('displays article count', () => {
    render(<NewsList articles={mockArticles} loading={false} error={null} />);
    const countText = screen.getByText(/2 articles found/i);
    expect(countText).toBeInTheDocument();
  });
});
