from crewai import Agent, Task, Crew
import os
from langchain.agents import Tool
from langchain.utilities import WikipediaAPIWrapper
from langchain.tools import DuckDuckGoSearchRun
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_community.tools import YouTubeSearchTool

load_dotenv()

# Initialize YouTube search tool
app = YouTubeSearchTool()

youtube = Tool(
    name="YouTubeSearch",
    func=app.run,
    description="Useful for when you need to answer questions about current events. Input should be a search query.",
)

# Setup API keys if needed (not required for Wikipedia or DuckDuckGo)
llm = ChatGroq(
    temperature=0,
    model_name="llama3-70b-8192",
    api_key="",
)

# Define the finder agent
finder = Agent(
    role="Finder",
    goal="Find best possible YouTube channel for learning a skill({topic}) from YouTube.",
    backstory="You are an agent that helps you find the best possible YouTube channel for learning a skill({topic}).",
    tools=[youtube],
    llm=llm 
)

# Create a task for the finder agent
finder_task = Task(
    name="Finder",
    description="Find best possible YouTube channel for learning a skill({topic}) from YouTube.",
    expected_output="Channel Name 1 link Channel Name 2 link" ,
    agent=finder,
    tools=[youtube]
)

# Assemble the crew
finder_crew = Crew(
    name="Finder",
    tasks=[finder_task],
    agents=[finder], 
    verbose=True
)

# Run the crew with the specified topic
result = finder_crew.kickoff({"topic": "python"})

# Print the result
print(result)