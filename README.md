# Animagen WebApp

Transform scientific concepts into stunning animations using AI-powered natural language processing.

## Features

- **Two-Step AI Generation**: Uses a Planner agent and an HTML Creator agent for high-quality, scientifically accurate animations.
- **Natural Language Input**: Describe animations in plain English - no technical skills required.
- **Mistral AI Integration**: Powered by Mistral's `devstral-medium-latest` for both planning and code generation.
- **Pure HTML+CSS+JS**: Self-contained animations with no external dependencies.
- **Scientific Accuracy**: Focused on educational value with physics-based rendering.
- **Async Processing**: Uses Python threading for background generation, ensuring a responsive chat interface.
- **Modern Frontend**: Interactive UI built with Next.js 16 and React 19.

## Architecture

### Backend (Django)
- **Django 6.0.2** with Django REST Framework.
- **Python Threading**: Handles background animation generation without requiring external workers like Redis or RabbitMQ.
- **Mistral AI API**: Orchestrates the animation generation process.
- **SQLite**: Default database for development.

### Frontend (Next.js)
- **Next.js 16.1.6** with App Router.
- **React 19.2.3**.
- **TypeScript 5**.
- **CSS Modules**: For encapsulated and maintainable styling.

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
   Edit `.env` and set your `MISTRAL_API_KEY`.

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Start the Django development server**
   ```bash
   python manage.py runserver
   ```
   The backend API will be available at `http://localhost:8000`.

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
   The frontend will be available at `http://localhost:3000`.

## Usage

### Creating an Animation
1. Open `http://localhost:3000`.
2. Start a new session.
3. Describe what you want to see (e.g., "Show me the interior of an atom" or "Visualize cellular respiration").
4. The system automatically detects animation requests and starts the generation process.
5. Once ready, click the "Animation Ready" card in the sidebar to view the result.

## API Endpoints

### Sessions
- `POST /api/sessions/` - Create a new session.
- `GET /api/sessions/<session_guid>/` - Get session details and messages.

### Messages
- `POST /api/sessions/<session_guid>/messages/` - Create a message (auto-detects animation requests).
- `GET /api/sessions/<session_guid>/messages/<message_id>/` - Poll for message status and retrieve HTML content.

## Animation Detection
The system automatically detects animation requests based on these keywords:
`animation`, `animate`, `show me`, `create`, `generate`, `make`, `visualize`, `demonstrate`, `illustrate`.

## Project Structure

```
animagen_webapp/
├── animagen/                    # Django app
│   ├── AnimaGen_Utils.py        # AnimationGenerator (Planner + HTML agents)
│   ├── models.py                # Session, Message, SessionHTML models
│   ├── views.py                 # API endpoints and keyword detection
│   ├── tasks.py                 # Background thread management
│   ├── serializers.py           # DRF serializers
│   └── urls.py                  # App-level routing
├── animagen_ai/                 # Django project settings
├── animagen_frontend/           # Next.js frontend
│   └── src/app/                 # App Router pages and components
├── requirements.txt             # Python dependencies
└── .env.example                # Environment variables template
```

## Troubleshooting

### Animation not appearing
1. **Check MISTRAL_API_KEY**: Ensure it's correctly set in your `.env` file.
2. **Check Server Logs**: Look for "Animation generated successfully" or error messages in the Django terminal.
3. **Keyword Check**: Ensure your prompt includes one of the detection keywords (e.g., "create").

## License
MIT License - see [LICENSE](LICENSE) for details.
