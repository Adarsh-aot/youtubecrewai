import streamlit as st
from crewai import Agent, Task, Crew , Process
from langchain.agents import Tool
from langchain_groq import ChatGroq
from langchain_community.tools import YouTubeSearchTool
from dotenv import load_dotenv

load_dotenv()

# Initialize YouTube search tool
app = YouTubeSearchTool()

youtube = Tool(
    name="YouTubeSearch",
    func=app.run,
    description="Useful for when you need to answer questions about current events. Input should be a search query.",
)

# Setup API keys if needed
llm = ChatGroq(
    temperature=0,
    model_name="llama3-70b-8192",
    api_key="",
)

# Define the finder agent
finder = Agent(
    role="Finder",
    goal="Find 2 best possible YouTube channel for learning a skill({topic}) from YouTube.",
    backstory="You are an agent that helps you find the best possible YouTube channel for learning a skill({topic}).",
    tools=[youtube],
    llm=llm 
)

# Create a task for the finder agent
finder_task = Task(
    name="Finder",
    description="Find 2 best possible YouTube channel for learning a skill({topic}) from YouTube.",
    expected_output="Channel Name 1 link Channel Name 2 link",
    agent=finder,
    tools=[youtube]
)

# Assemble the crew
finder_crew = Crew(
    name="Finder",
    tasks=[finder_task],
    agents=[finder], 
    process=Process.sequential,
    verbose=True
)

# Streamlit UI
st.title("YouTube Channel Finder")

topic = st.text_input("Enter a skill topic (e.g., Python):")

if st.button("Find Channels"):
    if topic:
        result = finder_crew.kickoff({"topic": topic})
        st.write("Results:")
        st.write(result)
    else:
        st.error("Please enter a topic to search.")