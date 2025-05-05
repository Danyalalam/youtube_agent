from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.reasoning import ReasoningTools
from agno.tools.youtube import YouTubeTools
from agno.playground import Playground, serve_playground_app
from agno.storage.sqlite import SqliteStorage
from dotenv import load_dotenv
import os
load_dotenv()

# Define storage location
agent_storage = "tmp/agents.db"

# Create the YouTube blog agent
youtube_blog_agent = Agent(
    name="YouTube Blog Generator",
    model=Gemini(id="gemini-2.5-flash-preview-04-17", api_key=os.getenv("Google_Api_Key")),
    tools=[
        ReasoningTools(add_instructions=True),
        YouTubeTools(),
    ],
    instructions=[
        "You are a professional blog writer who creates engaging, well-structured content based on YouTube videos.",
        "For each video URL provided:",
        "1. Extract and analyze the key points, themes, and insights from the video",
        "2. Structure the blog with a compelling introduction, clearly defined sections, and a conclusion",
        "3. Include relevant quotes or highlights from the video when appropriate",
        "4. Write in a conversational yet professional tone",
        "5. Include a brief summary of who created the video and their expertise",
        "6. Add appropriate headings and subheadings for readability",
        "7. End with thought-provoking questions or takeaways for the reader"
    ],
    storage=SqliteStorage(table_name="youtube_blog_agent", db_file=agent_storage),
    add_datetime_to_instructions=True,
    add_history_to_messages=True,
    num_history_responses=5,
    markdown=True,
)

# Create the playground with your agent
app = Playground(agents=[youtube_blog_agent]).get_app()

# Serve the app when script is run directly
if __name__ == "__main__":
    serve_playground_app("youtube_agent:app", reload=True)