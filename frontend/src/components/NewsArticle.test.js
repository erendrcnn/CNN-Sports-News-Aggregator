import React from 'react';
import { render, screen } from '@testing-library/react';
import NewsArticle from './NewsArticle';

describe('NewsArticle Component', () => {
  const mockArticle = {
    id: 1,
    title: 'Test Sports News Article',
    link: 'https://example.com/article',
    published_date: '2024-01-01T12:00:00Z',
    description: 'This is a test article description',
    source: 'CNN Sports',
  };

  test('renders article title', () => {
    render(<NewsArticle article={mockArticle} />);
    const titleElement = screen.getByText(/Test Sports News Article/i);
    expect(titleElement).toBeInTheDocument();
  });

  test('renders article link', () => {
    render(<NewsArticle article={mockArticle} />);
    const linkElement = screen.getByRole('link');
    expect(linkElement).toHaveAttribute('href', mockArticle.link);
  });

  test('renders article source', () => {
    render(<NewsArticle article={mockArticle} />);
    const sourceElement = screen.getByText(/CNN Sports/i);
    expect(sourceElement).toBeInTheDocument();
  });

  test('renders article description', () => {
    render(<NewsArticle article={mockArticle} />);
    const descriptionElement = screen.getByText(
      /This is a test article description/i
    );
    expect(descriptionElement).toBeInTheDocument();
  });
});
