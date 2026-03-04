import os
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from linkup import LinkupClient
from crewai import Crew, Agent, Task, Process, LLM
from crewai.tools import BaseTool

load_dotenv()

def get_llm_client() -> LLM:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables.")
    return LLM(
        model=os.getenv("GROQ_MODEL"),
        api_key=api_key,
        )

class LinkupSearchInput(BaseModel):
    query: str = Field(..., description="The search query to execute.")
    depth: str = Field(default="medium", description="The depth of the search: 'standard' or 'deep'")
    output_type: str = Field(default="searchResults", description="Output type: 'searchResults' or 'sourcedAnswer' or 'structured'")

class LinkupSearchTool(BaseTool):
    name: str = "linkup_search"
    description: str = "Search the web for information using LinkUp and return comprehensive results"
    args_schema: type[BaseModel] = LinkupSearchInput

    def __init__(self):
        super().__init__()

    def run(self, query, depth="standard", output_type="searchResults"):
        try:
            linkup_client = LinkupClient(api_key=os.getenv("LINKUP_API_KEY"))
            
            search_response = linkup_client.search(
                query=query,
                depth=depth,
                output_type=output_type
            )

            return str(search_response)
        except Exception as e:
            return f"Error during LinkUp search: {str(e)}"
        
def create_research_crew(query):
    linkup_search_tool = LinkupSearchTool()
    client = get_llm_client()
    
    web_searcher = Agent(
    role="Web Searcher",
    goal="Find the most relevant information on the web, along with source links (urls).",
    backstory="An expert at formulating search queries and retrieving relevant information. Passes the results to the 'Research Analyst' only.",
    verbose=True,
    allow_delegation=True,
    tools=[linkup_search_tool],
    llm=client,
    )

    research_analyst = Agent(
        role="Research Analyst",
        goal="Analyze and synthesize raw information into structured insights, along with source links (urls) as citations.",
        backstory="An expert at analyzing information, identifying patterns, and extracting key insights. If required, can delagate the task of fact checking/verification to 'Web Searcher' only. Passes the final results to the 'Technical Writer' only.",
        verbose=True,
        allow_delegation=True,
        llm=client,
    )

    technical_writer = Agent(
        role="Technical Writer",
        goal="Create well-structured, clear, and comprehensive responses in markdown format, with citations/source links (urls).",
        backstory="An expert at communicating complex information in an accessible way.",
        verbose=True,
        allow_delegation=False,
        llm=client,
    )

    search_task = Task(
        description=f"Search for comprehensive information about: {query}.",
        agent=web_searcher,
        expected_output="Detailed raw search results including sources (urls).",
        tools=[linkup_search_tool]
    )

    analysis_task = Task(
        description="Analyze the raw search results, identify key information, verify facts and prepare a structured analysis.",
        agent=research_analyst,
        expected_output="A structured analysis of the information with verified facts and key insights, along with source links",
        context=[search_task]
    )

    writing_task = Task(
        description="Create a comprehensive, well-organized response based on the research analysis.",
        agent=technical_writer,
        expected_output="A clear, comprehensive response that directly answers the query with proper citations/source links (urls).",
        context=[analysis_task]
    )

    crew = Crew(
        agents=[web_searcher, research_analyst, technical_writer],
        tasks=[search_task, analysis_task, writing_task],
        verbose=True,
        process=Process.sequential
    )

    return crew
        
def run_research(query):
    try:
        crew = create_research_crew(query)
        result = crew.kickoff()
        return result.raw;
    except Exception as e:
        print(f"Error occurred while running research for query '{query}': {str(e)}")