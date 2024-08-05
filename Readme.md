# README.md for YouTube Search CrewAI Project

## Introduction

This project demonstrates how to utilize CrewAI to create an agent-based system that finds the best YouTube channels for learning specific skills. The primary focus is on leveraging the YouTube search tool to provide users with relevant educational content.

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.6 or higher
- Pip, the Python package manager
- Required Python libraries (listed below)

## Installation

1. **Clone the Repository**: 
   Clone or download this repository to your local machine.

2. **Install Dependencies**: 
   Navigate to the project directory and install the required packages:

   ```bash
   pip install crewai langchain langchain_groq python-dotenv
   ```

3. **Set Up Environment Variables**: 
   Create a `.env` file in the project directory and add your API keys:

   ```
   API_KEY=your_api_key_here
   ```

   Replace `your_api_key_here` with your actual API key for the language model.

## Project Structure

The project contains the following key files:

- `crew.py`: The main script that initializes the CrewAI components and executes the task.
- `.env`: A file for storing environment variables securely.

## Code Overview

The main script, `crew.py`, sets up the CrewAI framework to find YouTube channels based on a specified topic. Here’s a brief overview of the code:

```python
from crewai import Agent, Task, Crew
from langchain.agents import Tool
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

# Setup API keys if needed
llm = ChatGroq(
    temperature=0,
    model_name="llama3-70b-8192",
    api_key="your_api_key_here",
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
    expected_output="Channel Name 1 link Channel Name 2 link",
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
```

### Explanation of Key Components

- **YouTubeSearchTool**: This tool is utilized to perform searches on YouTube based on user queries.
  
- **Agent**: The `Finder` agent is designed to locate the best YouTube channels for learning a specified skill.

- **Task**: A task is defined for the `Finder` agent, specifying what it needs to accomplish and the expected output format.

- **Crew**: The crew is assembled with the defined agent and task, ready to execute the search.

## Running the Project

To run the project, execute the following command in your terminal:

```bash
python crew.py
```

You can change the topic in the `kickoff` method to search for different skills.

## Conclusion

This project showcases the capabilities of CrewAI in creating collaborative AI agents that can assist users in finding educational resources. By leveraging YouTube's vast content, users can easily discover channels that suit their learning needs.

Feel free to expand upon this project by adding more features or integrating additional tools!

Citations:
[1] https://blog.gopenai.com/crewai-in-action-code-examples-for-building-your-first-crew-fac6f531b52c
[2] https://composio.dev/blog/crewai-examples/
[3] https://github.com/stephenc222/example-crewai
[4] https://www.youtube.com/watch?v=vhbfs38XmKk
[5] https://alejandro-ao.com/crew-ai-crash-course-step-by-step/