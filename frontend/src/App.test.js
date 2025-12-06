import React from 'react';
import { render } from '@testing-library/react';
import App from './App';

// Mock the newsApi service - getTodayNews returns an array directly
jest.mock('./services/newsApi', () => ({
  __esModule: true,
  default: {
    getTodayNews: jest.fn(() => Promise.resolve([])),
    refreshNews: jest.fn(() => Promise.resolve({ count: 0, results: [] })),
  },
}));

test('renders without crashing', () => {
  const { container } = render(<App />);
  expect(container).toBeInTheDocument();
});
