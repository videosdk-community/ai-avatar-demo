# Build Real-Time Video Avatars for Your App or Website in Minutes

This repository demonstrates integrating Simli avatar with VideoSDK Agent SDK, providing AI agents with a human-looking face for interactive voice and video conversations.

## Prerequisites

- Python 3.11+
- VideoSDK Account (https://app.videosdk.live/)
- Google API Key (https://aistudio.google.com/app/apikey)
- Simli FaceID & API Key (https://app.simli.com/)

## Project Structure

```
├── main.py              # Main agent implementation
├── requirements.txt     # Python dependencies
├── mcp_weather.py      # Weather MCP server
├── .env.example        # Environment variables template
└── README.md           # This file
```

## Getting Started

### 1. Create a virtual environment

```bash
python -m venv .venv
```

### 2. Activate the virtual environment

```bash
# On Windows
.venv\Scripts\activate

# On macOS/Linux
source .venv/bin/activate
```

### 3. Install requirements

```bash
python -m pip install -r requirements.txt
```

### 4. Add API keys

```bash
cp .env.example .env
```

Edit the `.env` file and add your API keys:

- `VIDEOSDK_AUTH_TOKEN`: Your VideoSDK authentication token
- `GOOGLE_API_KEY`: Your Google API key for Gemini
- `SIMLI_API_KEY`: Your Simli API key
- `SIMLI_FACE_ID`: Your Simli Face ID
- `OPENWEATHER_API_KEY` : accessing current weather using Model Context Protocol (MCP)

### 5. Run VideoSDK agent worker

```bash
python main.py
```

## Output

After running the agent, you'll get a link in the format:

```
https://playground.videosdk.live?token=...&meetingId=...
```

For reference: https://docs.videosdk.live/ai_agents/playground

## Features

- Real-time AI voice conversation with human-like avatar
- Google Gemini integration for natural language processing
- Simli avatar for visual representation
- Weather information through MCP (Model Context Protocol)
- Interactive playground for testing

## Usage

1. Start the agent by running `python main.py`
2. Open the provided playground URL in your browser
3. Start talking to your AI avatar assistant
4. Ask questions about weather or general topics

## VideoSDK Agents

Build and deploy production-ready AI voice & video agents with [VideoSDK](https://videosdk.live). This repo is your central hub for agent templates, feature examples, and everything you need to ship real-world AI-powered applications.

| Resource | Description |
|---|---|
| 🚀 [Use Case Examples](https://github.com/videosdk-live/agents/tree/main/use_case_examples) | Production-ready templates across Customer Support, Healthcare, Tech Support & more |
| ⚡ [Feature Examples](https://github.com/videosdk-live/agents/tree/main/examples) | Always up-to-date examples showcasing the latest VideoSDK Agent features |
| 📖 [AI Agents Docs](https://docs.videosdk.live/ai_agents/introduction) | Full guides, concepts & API references to get you started |

> ⭐ If this helps you, star this repo and [`videosdk-live/agents`](https://github.com/videosdk-live/agents) — it keeps us motivated to ship more!

## License

This project is open source and available under the MIT License.
