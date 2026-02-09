# Contributing Guidelines

Thank you for considering contributing to Endee RAG & Semantic Search! This document outlines the process and guidelines.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/endee-rag-app.git`
3. Create a branch: `git checkout -b feature/your-feature`
4. Make changes and commit: `git commit -m "Add your feature"`
5. Push to your fork: `git push origin feature/your-feature`
6. Open a Pull Request

## Code Style

### Python (Backend)

```bash
# Format code
black backend/
isort backend/

# Lint
pylint backend/*.py
```

### JavaScript (Frontend)

```bash
# Format
npx prettier --write frontend/src/

# Lint
npm run lint
```

## Testing

```bash
# Backend
pytest backend/tests/ -v

# Frontend
npm test
```

## Commit Messages

Use conventional commits:
```
feat: add new feature
fix: resolve bug
docs: update documentation
refactor: improve code structure
test: add test cases
```

Example:
```
feat(api): add document delete endpoint
```

## Pull Request Process

1. Ensure tests pass
2. Update documentation if needed
3. Provide clear PR description
4. Request review from maintainers
5. Address feedback and iterate

## Issues

Report bugs or suggest features via GitHub Issues with:
- Clear description
- Steps to reproduce (for bugs)
- Expected vs actual behavior
- Environment details (OS, versions)

Thank you for contributing! 🎉
