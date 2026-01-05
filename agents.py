"""
LifeOps AI Agents using CrewAI with Google Gemini
"""
import os
from typing import List, Optional
from crewai import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI

# Load environment variables
load_dotenv()

class LifeOpsAgents:
    """Container for all LifeOps AI agents"""
    
    def __init__(self):
        # Initialize Google Gemini LLM
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        # Initialize LLM directly for CrewAI compatibility
        self.llm = GoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=api_key,
            temperature=0.7,
            max_tokens=None,
            timeout=None,
            max_retries=2,
        )
        
        # Alternative: Using ChatGoogleGenerativeAI if the above doesn't work
        self.chat_llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.7,
            google_api_key=api_key
        )
    
    def create_health_agent(self) -> Agent:
        """Create the Health & Wellness Agent"""
        return Agent(
            role="Health and Wellness Expert",
            goal="""Optimize user's physical and mental health through balanced routines,
                  stress management, sleep optimization, and nutrition advice.""",
            backstory="""You are Dr. Maya Patel, a holistic health expert with 15 years of 
                       experience in preventive medicine and stress management. You combine 
                       Eastern wellness traditions with Western medical science to create 
                       sustainable health routines. You believe that optimal health is the 
                       foundation for all life success.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,  # Using Google Gemini
            max_iter=3,
            max_rpm=10
        )
    
    def create_finance_agent(self) -> Agent:
        """Create the Personal Finance Agent"""
        return Agent(
            role="Personal Finance Advisor",
            goal="""Help users manage their finances effectively, create budgets, 
                  optimize expenses, and build savings while maintaining quality of life.""",
            backstory="""You are Alex Chen, a certified financial planner who specializes 
                       in helping professionals balance ambition with financial stability. 
                       You've helped hundreds of clients achieve financial independence 
                       through smart budgeting and investment strategies. You believe money 
                       should enable life goals, not control them.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,  # Using Google Gemini
            max_iter=3,
            max_rpm=10
        )
    
    def create_study_agent(self) -> Agent:
        """Create the Learning & Productivity Agent"""
        return Agent(
            role="Learning and Productivity Specialist",
            goal="""Design effective study schedules, optimize learning techniques, 
                  manage time efficiently, and prevent burnout while achieving academic goals.""",
            backstory="""You are Professor James Wilson, an educational psychologist 
                       with expertise in cognitive science and time management. You've 
                       published research on optimal learning intervals and helped 
                       thousands of students achieve academic success without burnout. 
                       You believe smart work always beats hard work.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,  # Using Google Gemini
            max_iter=3,
            max_rpm=10
        )
    
    def create_life_coordinator(self) -> Agent:
        """Create the Master Life Coordinator Agent"""
        return Agent(
            role="Life Operations Coordinator",
            goal="""Orchestrate all life domains (health, finance, study) to create 
                  a balanced, sustainable lifestyle. Make trade-off decisions when 
                  conflicts arise between domains.""",
            backstory="""You are Sophia Williams, a renowned life strategist who 
                       integrates multiple life domains into cohesive strategies. 
                       With degrees in psychology, business, and education, you 
                       understand how different life areas interact. Your specialty 
                       is making tough decisions that optimize for long-term happiness 
                       and success.""",
            verbose=True,
            allow_delegation=True,
            llm=self.llm,  # Using Google Gemini
            max_iter=5,
            max_rpm=15
        )
    
    def get_all_agents(self) -> List[Agent]:
        """Get all agents as a list"""
        return [
            self.create_health_agent(),
            self.create_finance_agent(),
            self.create_study_agent(),
            self.create_life_coordinator()
        ]
