"""
LifeOps AI Tasks for CrewAI
"""
from crewai import Task
from typing import Dict, Any
from agents import LifeOpsAgents
from datetime import datetime

class LifeOpsTasks:
    """Container for all LifeOps AI tasks"""
    
    def __init__(self, user_context: Dict[str, Any]):
        self.user_context = user_context
        self.agents = LifeOpsAgents()
    
    def create_health_analysis_task(self) -> Task:
        """Task for health agent to analyze user's health status"""
        health_agent = self.agents.create_health_agent()
        
        return Task(
            description=f"""Analyze the user's health situation comprehensively:
            
            User Context:
            - Stress Level: {self.user_context.get('stress_level', 'Not specified')}/10
            - Sleep Pattern: {self.user_context.get('sleep_hours', 'Not specified')} hours
            - Exercise Frequency: {self.user_context.get('exercise_frequency', 'Not specified')}
            - Problem: {self.user_context.get('problem', 'No specific problem mentioned')}
            
            Your Analysis Should Include:
            1. Current health risk assessment
            2. Immediate stress reduction strategies
            3. Sleep optimization plan
            4. Quick exercise/movement recommendations
            5. Nutrition tips for stress management
            
            Consider cross-domain impacts:
            - How health affects study productivity
            - How health decisions impact finances
            - Time allocation for health vs other activities
            
            Format your output with clear sections and actionable steps.
            """,
            agent=health_agent,
            expected_output="""A comprehensive health analysis with actionable steps."""
        )
    
    def create_finance_analysis_task(self) -> Task:
        """Task for finance agent to analyze user's financial situation"""
        finance_agent = self.agents.create_finance_agent()
        
        return Task(
            description=f"""Analyze the user's financial situation and provide guidance:
            
            User Context:
            - Monthly Budget: ${self.user_context.get('monthly_budget', 'Not specified')}
            - Current Expenses: ${self.user_context.get('current_expenses', 'Not specified')}
            - Financial Goals: {self.user_context.get('financial_goals', 'Not specified')}
            - Problem: {self.user_context.get('problem', 'No specific problem mentioned')}
            
            Your Analysis Should Include:
            1. Budget allocation analysis
            2. Expense optimization opportunities
            3. Savings strategy
            4. Emergency fund recommendations
            
            Consider cross-domain impacts:
            - How financial decisions affect health (stress, nutrition)
            - Budget allocation for study materials/courses
            - Financial stress impact on overall wellbeing
            
            Provide specific, actionable financial advice.
            """,
            agent=finance_agent,
            expected_output="""A detailed financial plan with actionable advice."""
        )
    
    def create_study_analysis_task(self) -> Task:
        """Task for study agent to analyze user's learning situation"""
        study_agent = self.agents.create_study_agent()
        
        days_until_exam = self.user_context.get('days_until_exam', 0)
        exam_date = self.user_context.get('exam_date', 'Not specified')
        
        return Task(
            description=f"""Analyze the user's study situation and create an optimal plan:
            
            User Context:
            - Upcoming Exam: {exam_date} ({days_until_exam} days from now)
            - Current Study Hours: {self.user_context.get('current_study_hours', 'Not specified')}/day
            - Subjects/Topics: {self.user_context.get('subjects', 'Not specified')}
            - Problem: {self.user_context.get('problem', 'No specific problem mentioned')}
            
            Your Analysis Should Include:
            1. Study schedule optimization
            2. Effective learning techniques for retention
            3. Burnout prevention strategies
            4. Break scheduling recommendations
            
            Consider cross-domain impacts:
            - How study schedule affects sleep/health
            - Financial investment in study resources
            - Stress management during study periods
            
            Create a realistic, sustainable study plan.
            """,
            agent=study_agent,
            expected_output="""A comprehensive study plan with schedule and techniques."""
        )
    
    def create_life_coordination_task(self, context_tasks: list) -> Task:  # FIXED INDENTATION
        """Master task that coordinates all domains"""
        coordinator = self.agents.create_life_coordinator()
        
        return Task(
            description=f"""Integrate insights from all domains and create a unified life plan.
            
            User's Problem: {self.user_context.get('problem', 'General life optimization')}
            
            Important: Provide CROSS-DOMAIN REASONING like:
            - "Because stress is high, reduce study hours"
            - "Since budget is tight, prioritize free health activities"
            - "Given the exam is soon, adjust sleep schedule accordingly"
            
            Create a balanced weekly schedule with specific actions.
            
            Cross-domain insights are CRITICAL for this task.
            """,
            agent=coordinator,
            expected_output="A unified life plan with cross-domain reasoning and specific actions.",
            context=context_tasks
        )
