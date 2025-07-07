import asyncio
import sys
from pathlib import Path
import requests
from videosdk.agents import Agent, AgentSession, RealTimePipeline, JobContext, RoomOptions, WorkerJob, MCPServerStdio
from videosdk.plugins.google import GeminiRealtime, GeminiLiveConfig
from videosdk.plugins.simli import SimliAvatar, SimliConfig
from dotenv import load_dotenv
import os

load_dotenv(override=True)

def get_room_id(auth_token: str) -> str:
    url = "https://api.videosdk.live/v2/rooms"
    headers = {
        "Authorization": auth_token
    }
    response = requests.post(url, headers=headers)
    response.raise_for_status()
    return response.json()["roomId"]

class MyVoiceAgent(Agent):
    def __init__(self):
        mcp_script_weather = Path(__file__).parent / "mcp_weather.py"
        super().__init__(
            instructions="You are VideoSDK's AI Avatar Voice Agent with real-time capabilities. You are a helpful virtual assistant with a visual avatar that can answer questions about weather help with other tasks in real-time.",
            mcp_servers = [
                MCPServerStdio(
                command=sys.executable,
                args=[str(mcp_script_weather)],
                client_session_timeout_seconds=30
                )
                ]
        )

    async def on_enter(self) -> None:
        await self.session.say("Hello! I'm your real-time AI avatar assistant. How can I help you today?")
    
    async def on_exit(self) -> None:
        await self.session.say("Goodbye! It was great talking with you!")
        

async def start_session(context: JobContext):
    # Initialize Gemini Realtime model
    model = GeminiRealtime(
        model="gemini-2.0-flash-live-001",
        # When GOOGLE_API_KEY is set in .env - DON'T pass api_key parameter
        api_key="AIzaSyBHRRbLb280VP4bj7sYN1tuJJSFRjxrKrY", 
        config=GeminiLiveConfig(
            voice="Leda",  # Puck, Charon, Kore, Fenrir, Aoede, Leda, Orus, and Zephyr.
            response_modalities=["AUDIO"]
        )
    )

    # Initialize Simli Avatar
    simli_config = SimliConfig(
        apiKey="l7g8sozma6clp3ecefwb6",
    )
    simli_avatar = SimliAvatar(config=simli_config)

    # Create pipeline with avatar
    pipeline = RealTimePipeline(
        model=model,
        avatar=simli_avatar
    )
    
    session = AgentSession(
        agent=MyVoiceAgent(),
        pipeline=pipeline
    )

    try:
        await context.connect()
        await session.start()
        await asyncio.Event().wait()
    finally:
        await session.close()
        await context.shutdown()

def make_context() -> JobContext:
    auth_token = os.getenv("VIDEOSDK_AUTH_TOKEN")
    room_id = get_room_id(auth_token)
    room_options = RoomOptions(
        room_id=room_id,
        auth_token=auth_token,
        name="Simli Avatar Realtime Agent",
        playground=True 
    )
    return JobContext(room_options=room_options)


if __name__ == "__main__":
    job = WorkerJob(entrypoint=start_session, jobctx=make_context)
    job.start() 