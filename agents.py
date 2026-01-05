"""
LifeOps AI Agents using CrewAI with Google Gemini
"""
import os
from crewai import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class LifeOpsAgents:
    """Container for all LifeOps AI agents"""
    
    def __init__(self):
        # Get API key
        api_key = os.getenv("GOOGLE_API_KEY")
        
        # IMPORTANT: Set dummy OpenAI key to prevent CrewAI from using OpenAI
        os.environ["OPENAI_API_KEY"] = "not-needed"
        os.environ["OPENAI_MODEL_NAME"] = "not-needed"
        
        if not api_key or api_key == "your_google_api_key_here":
            raise ValueError("❌ GOOGLE_API_KEY not found. Please add it in Streamlit Cloud Secrets.")
        
        # Initialize Gemini LLM - USE gemini-pro instead of gemini-1.5-flash
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-pro",  # CHANGED: More reliable model
            google_api_key=api_key,
            temperature=0.7,
            max_tokens=2048
        )
        
        print(f"✅ Using Google Gemini: gemini-pro")
    
    def create_health_agent(self) -> Agent:
        """Create the Health & Wellness Agent"""
        return Agent(
            role="Health and Wellness Expert",
            goal="Optimize user's physical and mental health through balanced routines, stress management, sleep optimization, and nutrition advice.",
            backstory="You are Dr. Maya Patel, a holistic health expert with 15 years of experience in preventive medicine and stress management.",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            max_iter=2
        )
    
    def create_finance_agent(self) -> Agent:
        """Create the Personal Finance Agent"""
        return Agent(
            role="Personal Finance Advisor",
            goal="Help users manage their finances effectively, create budgets, optimize expenses, and build savings.",
            backstory="You are Alex Chen, a certified financial planner who specializes in helping professionals balance ambition with financial stability.",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            max_iter=2
        )
    
    def create_study_agent(self) -> Agent:
        """Create the Learning & Productivity Agent"""
        return Agent(
            role="Learning and Productivity Specialist",
            goal="Design effective study schedules, optimize learning techniques, manage time efficiently, and prevent burnout.",
            backstory="You are Professor James Wilson, an educational psychologist with expertise in cognitive science and time management.",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            max_iter=2
        )
    
    def create_life_coordinator(self) -> Agent:
        """Create the Master Life Coordinator Agent"""
        return Agent(
            role="Life Operations Coordinator",
            goal="Orchestrate all life domains (health, finance, study) to create a balanced, sustainable lifestyle.",
            backstory="You are Sophia Williams, a renowned life strategist who integrates multiple life domains into cohesive strategies.",
            verbose=True,
            allow_delegation=True,
            llm=self.llm,
            max_iter=3
        )
