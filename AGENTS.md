# Animagen WebApp - Agent Guidelines

This document provides build, test, lint commands and code style guidelines for the animagen_webapp project.

## Project Structure

- `animagen_ai/` - Django project configuration
- `animagen/` - Django app (models, views, tests, serializers, tasks, utils)
- `animagen_frontend/` - Next.js 16 frontend (TypeScript + React 19)

## Animation Generation System

Uses Mistral's "devstral-medium-latest" model to generate HTML+CSS+JS animations. Flow: user message → `isPending=True` → Django Q background task → Mistral API → save to `SessionHTML` → update message with `isPending=False`.

**API Endpoints:**
- `POST /api/sessions/<session_guid>/messages/` - Create message (auto-detects animation)
- `POST /api/sessions/<session_guid>/messages/<message_id>/generate-animation/` - Manual trigger
- `GET /api/sessions/<session_guid>/` - Get session with HTML content

## Build/Lint/Test Commands

### Frontend (animagen_frontend/)
```bash
npm run dev      # Start dev server (localhost:3000)
npm run build    # Build for production
npm start        # Start production server
npm run lint     # Run ESLint
```

### Backend (Django)
```bash
python manage.py runserver              # Start dev server
python manage.py test                   # Run all tests
python manage.py test animagen          # Run animagen tests
python manage.py test animagen.tests.TestClassName        # Run specific class
python manage.py test animagen.tests.TestClassName.test_method  # Run single test
python manage.py migrate                # Apply migrations
python manage.py makemigrations         # Create migrations
python manage.py qcluster              # Start Django Q worker
```

## Code Style Guidelines

### Python (Django)

**Naming:** Classes PascalCase, functions/variables snake_case, constants UPPER_SNAKE_CASE

**Imports:** Group as standard lib, third-party, local. Use `from pathlib import Path` for paths

**Type Hints:** Use type hints for function signatures (e.g., `def task(id: str) -> dict`)

**Django Patterns:**
- Models inherit from `django.db.models.Model`
- Use `get_object_or_404()` for 404 responses
- Use `BASE_DIR / 'subdir'` for path construction
- Define module-level constants (e.g., `MAX_FILE_SIZE = 10 * 1024 * 1024`)
- Use `logger = logging.getLogger(__name__)` for logging
- Views use decorators: `@api_view(["GET"])`, `@permission_classes([AllowAny])`
- Tests inherit from `django.test.TestCase`, use `setUp()` for initialization

**Error Handling:**
- Try/catch blocks with specific exception types
- Use `status.HTTP_400_BAD_REQUEST`, `status.HTTP_404_NOT_FOUND`, etc.
- Log errors with `logger.error()` or `logger.exception()`

### TypeScript/React (Next.js)

**Naming:** Components PascalCase, functions/variables camelCase, types/interfaces PascalCase

**Imports:** Use `import type` for type-only imports. Group: React/Next.js, third-party, local. Use path alias `@/*` for `./src/*`

**Components:**
- Functional components with React hooks
- Type props explicitly: `interface Props { title: string }`
- Use `Readonly<>` for props interfaces
- Prefer named exports
- Server components by default, use `"use client"` for interactive components
- Use hooks: `useState`, `useEffect`, `useRef`, `useCallback`

**TypeScript:** Strict mode enabled, avoid `any` type, define return types implicitly

**Styling:**
- CSS Modules with PascalCase class names: `import styles from "./page.module.css"`
- CSS variables for theming in `src/app/globals.css`
- Dark mode support via `@media (prefers-color-scheme: dark)`
- Geist fonts from `next/font/google` with CSS variables

**API Integration:**
- Base URL: `http://localhost:8000/api/`
- Use `fetch()` for API calls
- Poll pending messages with `setInterval()` (5s interval, 120s timeout)
- Use `useRef` for interval IDs to cleanup in `useEffect`

## General Guidelines

**Security:** Never commit secrets, use `.env` for config, validate inputs, sanitize HTML outputs (use `re.sub` for dangerous patterns)

**Testing:** Write tests for critical logic, use descriptive names, mock external dependencies, skip tests with `self.skipTest()` when dependencies unavailable

**Error Handling:** User-friendly messages, proper HTTP status codes (400, 404, 500), log errors appropriately

**Comments:** Add only when necessary, keep concise, document complex logic

**Git:** Meaningful commit messages, atomic commits, run linting before committing
