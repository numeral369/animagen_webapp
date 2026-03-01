# Animagen WebApp

Transform scientific concepts into stunning animations using AI-powered natural language processing.

## Features

- **Natural Language Input**: Describe animations in plain English - no technical skills required
- **AI-Powered Generation**: Uses Mistral's "devstral-medium-latest" model to generate animations
- **Pure HTML+CSS+JS**: Self-contained animations with no external dependencies
- **Scientific Accuracy**: Physics-based rendering for accurate representations
- **Real-time Processing**: Async background tasks for instant generation
- **Chat Interface**: Interactive frontend built with Next.js 16 and React 19

## Architecture

### Backend (Django)
- Django 6.0.2 with Django REST Framework
- Django Q for background task processing
- Mistral AI API for animation generation
- SQLite database (development)

### Frontend (Next.js)
- Next.js 16.1.6 with App Router
- React 19.2.3
- TypeScript 5
- CSS Modules for styling

## Setup

### Prerequisites

- Python 3.12+
- Node.js 18+
- Mistral API key

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd animagen_webapp
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   Copy `.env.example` to `.env` and add your Mistral API key:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and set your API key:
   ```
   MISTRAL_API_KEY=your-mistral-api-key-here
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Start the Django Q worker** (required for animation generation)
   ```bash
   python manage.py qcluster
   ```
   Keep this terminal open to process background tasks.

6. **Start the Django development server** (in a new terminal)
   ```bash
   python manage.py runserver
   ```

The backend API will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to the frontend directory**
   ```bash
   cd animagen_frontend
   ```

2. **Install Node.js dependencies**
   ```bash
   npm install
   ```

3. **Start the development server**
   ```bash
   npm run dev
   ```

The frontend will be available at `http://localhost:3000`

## Usage

### Creating an Animation

1. Open the web application at `http://localhost:3000`
2. Click "Start Creating" to create a new session
3. Describe what you want to see using natural language, for example:
   - "Show me the interior of an atom"
   - "Create an animation of planetary orbits"
   - "Visualize cellular respiration"
   - "Demonstrate quantum entanglement"
4. Send the message and wait for the AI to generate the animation
5. The generated animation will appear in the chat interface

### Manual Animation Generation

You can also manually trigger animation generation for any user message:

```bash
POST /api/sessions/<session_guid>/messages/<message_id>/generate-animation/
```

## API Endpoints

### Sessions
- `POST /api/sessions/` - Create a new session
- `GET /api/sessions/<session_guid>/` - Get session details and messages

### Messages
- `POST /api/sessions/<session_guid>/messages/` - Create a message (auto-detects animation requests)
- `POST /api/sessions/<session_guid>/messages/<message_id>/generate-animation/` - Manually trigger animation generation

## Animation Detection

The system automatically detects animation requests based on these keywords:
- "animation"
- "animate"
- "show me"
- "create"
- "generate"
- "make"
- "visualize"
- "demonstrate"
- "illustrate"

If a message contains any of these keywords, the animation generation process starts automatically.

## Project Structure

```
animagen_webapp/
├── animagen/                    # Django app
│   ├── Animagen_Utils.py        # AnimationGenerator class
│   ├── models.py                # Django models (Session, Message, SessionHTML)
│   ├── views.py                 # API views
│   ├── serializers.py           # DRF serializers
│   ├── tasks.py                 # Background tasks for animation generation
│   └── urls.py                  # URL patterns
├── animagen_ai/                 # Django project settings
│   ├── settings.py              # Django configuration
│   └── urls.py                 # Root URL configuration
├── animagen_frontend/           # Next.js frontend
│   ├── src/
│   │   └── app/                # App Router pages
│   │       ├── page.tsx         # Home page
│   │       └── session/[sessionGUID]/page.tsx  # Session chat page
│   └── package.json
├── requirements.txt             # Python dependencies
└── .env.example                # Environment variables template
```

## Development

### Running Tests

**Backend tests:**
```bash
python manage.py test
```

**Frontend linting:**
```bash
cd animagen_frontend
npm run lint
```

### Code Style

- Python: Follow Django conventions and PEP 8
- TypeScript/React: Follow React best practices with functional components
- Use CSS Modules for component styling

## Troubleshooting

### Animation generation not working

1. **Check if Django Q worker is running**
   - Ensure `python manage.py qcluster` is running in a separate terminal
   - Check that no errors are displayed in the worker terminal

2. **Verify MISTRAL_API_KEY is set**
   - Check your `.env` file contains a valid Mistral API key
   - Ensure the API key has not expired

3. **Check message is recognized as animation request**
   - Ensure your message contains animation keywords
   - Try using words like "create", "show me", or "animation"

### Frontend connection issues

1. **CORS errors**: Ensure `CORS_ALLOW_ALL_ORIGINS = True` in `animagen_ai/settings.py` (development only)

2. **Backend not running**: Ensure `python manage.py runserver` is running on port 8000

## License

[Your License Here]

## Contributing

[Your Contributing Guidelines Here]
