# Quick Start Guide

## Get the Animation Generation System Running in 5 Minutes

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Key

Create a `.env` file in the project root:

```bash
MISTRAL_API_KEY=your-api-key-here
```

Get your API key from: https://console.mistral.ai/

### 3. Setup Database

```bash
python manage.py migrate
```

### 4. Start Services

You'll need **two terminals**:

**Terminal 1 - Start Django Q Worker:**
```bash
python manage.py qcluster
```

**Terminal 2 - Start Django Server:**
```bash
python manage.py runserver
```

**Terminal 3 - Start Frontend (optional):**
```bash
cd animagen_frontend
npm install  # if not already installed
npm run dev
```

### 5. Generate Your First Animation

**Option A: Using the API**

```bash
curl -X POST http://localhost:8000/api/sessions/ \
  -H "Content-Type: application/json" \
  -d '{"title": "My Animation Session"}'
```

Copy the `sessionGUID` from the response, then:

```bash
curl -X POST http://localhost:8000/api/sessions/<sessionGUID>/messages/ \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "content=Create an animation of a bouncing ball"
```

**Option B: Using the Frontend**

1. Open http://localhost:3000
2. Click "Start Creating"
3. Type: "Create an animation of a bouncing ball"
4. Send and wait for the AI to generate your animation

### 6. View the Result

The animation will appear in the chat interface or API response as self-contained HTML code.

## Common Issues

**"MISTRAL_API_KEY not found"**
- Make sure you created the `.env` file
- Restart the Django server after adding the key

**"Animation not generating"**
- Ensure Django Q worker is running (Terminal 1)
- Check that your message contains animation keywords like "create", "show me", "animation"

**"Connection refused"**
- Make sure both Django server and qcluster are running
- Check they're running on different terminals

## Animation Keywords

These words will trigger animation generation:
- "animation"
- "animate"
- "show me"
- "create"
- "generate"
- "make"
- "visualize"
- "demonstrate"
- "illustrate"

## Example Prompts

- "Create an animation of a solar system"
- "Show me how a black hole works"
- "Visualize cellular respiration"
- "Generate a bouncing ball animation"
- "Demonstrate quantum entanglement"
- "Illustrate the water cycle"

## Next Steps

1. Explore the frontend interface
2. Try different animation prompts
3. Check out the API documentation in README.md
4. Read IMPLEMENTATION.md for technical details

Happy animating! 🎬
