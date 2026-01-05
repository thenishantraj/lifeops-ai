"""
LifeOps AI Agents using CrewAI
"""
import os
from typing import List, Optional
from crewai import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class LifeOpsAgents:
    """Container for all LifeOps AI agents"""
    
    def __init__(self):
        # Gemini Model Configuration
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            temperature=0.7,
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        
    def create_health_agent(self) -> Agent:
        return Agent(
            role="Health and Wellness Expert",
            goal="Optimize user's physical and mental health...",
            backstory="You are Dr. Maya Patel...",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            function_calling_llm=self.llm,  # <--- YE LINE JADU KAREGI (OpenAI ko rokegi)
            max_iter=3,
            max_rpm=10
        )
    
    def create_finance_agent(self) -> Agent:
        return Agent(
            role="Personal Finance Advisor",
            goal="Help users manage their finances...",
            backstory="You are Alex Chen...",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            function_calling_llm=self.llm,  # <--- YE LINE JADU KAREGI
            max_iter=3,
            max_rpm=10
        )
    
    def create_study_agent(self) -> Agent:
        return Agent(
            role="Learning and Productivity Specialist",
            goal="Design effective study schedules...",
            backstory="You are Professor James Wilson...",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            function_calling_llm=self.llm,  # <--- YE LINE JADU KAREGI
            max_iter=3,
            max_rpm=10
        )
    
    def create_life_coordinator(self) -> Agent:
        return Agent(
            role="Life Operations Coordinator",
            goal="Orchestrate all life domains...",
            backstory="You are Sophia Williams...",
            verbose=True,
            allow_delegation=False,  # <--- Ye False hi rahne dena
            llm=self.llm,
            function_calling_llm=self.llm,  # <--- YE LINE JADU KAREGI
            max_iter=5,
            max_rpm=15
        )
    
    def get_all_agents(self) -> List[Agent]:
        return [
            self.create_health_agent(),
            self.create_finance_agent(),
            self.create_study_agent(),
            self.create_life_coordinator()
        ]
