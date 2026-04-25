import sys
from pathlib import Path
from videosdk.agents import Agent, AgentSession, Pipeline, JobContext, RoomOptions, WorkerJob, MCPServerStdio
from videosdk.plugins.google import GeminiRealtime, GeminiLiveConfig
from videosdk.plugins.simli import SimliAvatar, SimliConfig
from dotenv import load_dotenv
import os
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", handlers=[logging.StreamHandler()])


load_dotenv(override=True)

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
        model="gemini-3.1-flash-live-preview",
        # When GOOGLE_API_KEY is set in .env - DON'T pass api_key parameter
        api_key=os.getenv("GOOGLE_API_KEY"),
        config=GeminiLiveConfig(
            voice="Leda",  # Puck, Charon, Kore, Fenrir, Aoede, Leda, Orus, and Zephyr.
            response_modalities=["AUDIO"]
        )
    )

    # Initialize Simli Avatar
    simli_config = SimliConfig(
        apiKey="l7g8sozma6clp3ecefwb6",
        faceId="0c2b8b04-5274-41f1-a21c-d5c98322efa9" # default
    )
    simli_avatar = SimliAvatar(config=simli_config)

    # Create pipeline with avatar
    pipeline = Pipeline(
        llm=model,
        avatar=simli_avatar
    )
    
    session = AgentSession(
        agent=MyVoiceAgent(),
        pipeline=pipeline
    )

    await session.start(wait_for_participant=True, run_until_shutdown=True)

def make_context() -> JobContext:
    room_options = RoomOptions(
        name="Simli Avatar Realtime Agent",
        playground=True
    )
    return JobContext(room_options=room_options)


if __name__ == "__main__":
    job = WorkerJob(entrypoint=start_session, jobctx=make_context)
    job.start() 
