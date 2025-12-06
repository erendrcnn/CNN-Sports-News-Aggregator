# Contributing to CNN Sports News Aggregator

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/TEST.git
   cd TEST
   ```

3. Set up the development environment:
   ```bash
   # On Windows (PowerShell)
   .\setup.ps1
   
   # On Unix/Linux/Mac
   chmod +x setup.sh
   ./setup.sh
   ```

## Code Style

### Python (Backend)
- Follow PEP 8 style guide
- Use Black for code formatting
- Use flake8 for linting
- Maximum line length: 88 characters
- Write docstrings for all functions and classes

### JavaScript (Frontend)
- Use ES6+ syntax
- Follow Airbnb JavaScript Style Guide
- Use Prettier for code formatting
- Use ESLint for linting
- Write JSDoc comments for complex functions

## Pre-commit Hooks

Install pre-commit hooks before making changes:

```bash
pip install pre-commit
pre-commit install
```

This will automatically format and lint your code before each commit.

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Pull Request Process

1. Create a new branch for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and commit:
   ```bash
   git add .
   git commit -m "Description of your changes"
   ```

3. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

4. Create a Pull Request on GitHub

### PR Requirements
- All tests must pass
- Code coverage should not decrease
- Follow SOLID principles
- Update documentation if needed
- Add tests for new features

## Commit Message Guidelines

Use conventional commits format:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting)
- `refactor:` Code refactoring
- `test:` Adding or updating tests
- `chore:` Maintenance tasks

Example:
```
feat: add pagination to news list
fix: resolve date filtering issue in RSS parser
docs: update API documentation
```

## Questions?

Feel free to open an issue for any questions or concerns.
