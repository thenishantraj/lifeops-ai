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
            - Diet Quality: {self.user_context.get('diet_quality', 'Not specified')}
            - Problem: {self.user_context.get('problem', 'No specific problem mentioned')}
            
            Your Analysis Should Include:
            1. Current health risk assessment
            2. Immediate stress reduction strategies
            3. Sleep optimization plan
            4. Quick exercise/movement recommendations
            5. Nutrition tips for stress management
            6. Warning signs to watch for
            
            Consider cross-domain impacts:
            - How health affects study productivity
            - How health decisions impact finances
            - Time allocation for health vs other activities
            
            Format your output with clear sections and actionable steps.
            """,
            agent=health_agent,
            expected_output="""A comprehensive health analysis with:
            1. Risk Assessment (Low/Medium/High)
            2. Immediate Actions (next 24 hours)
            3. Short-term Plan (next week)
            4. Long-term Recommendations
            5. Cross-domain Considerations
            """
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
            5. Cost-effective health/study investments
            
            Consider cross-domain impacts:
            - How financial decisions affect health (stress, nutrition)
            - Budget allocation for study materials/courses
            - Financial stress impact on overall wellbeing
            
            Provide specific, actionable financial advice.
            """,
            agent=finance_agent,
            expected_output="""A detailed financial plan with:
            1. Budget Allocation Breakdown
            2. Expense Optimization Tips
            3. Savings Strategy
            4. Investment Recommendations (if any)
            5. Cross-domain Financial Implications
            """
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
            5. Resource allocation
            
            Consider cross-domain impacts:
            - How study schedule affects sleep/health
            - Financial investment in study resources
            - Stress management during study periods
            
            Create a realistic, sustainable study plan.
            """,
            agent=study_agent,
            expected_output="""A comprehensive study plan with:
            1. Daily/Weekly Schedule
            2. Learning Technique Recommendations
            3. Progress Tracking Methods
            4. Break/Burnout Prevention Strategy
            5. Resource Recommendations
            6. Cross-domain Considerations
            """
        )
    
    def create_life_coordination_task(self, health_output: str, finance_output: str, study_output: str) -> Task:
        """Master task that coordinates all domains"""
        coordinator = self.agents.create_life_coordinator()
        
        return Task(
            description=f"""You are the Life Operations Coordinator. Your job is to integrate
            insights from all domains and create a unified life plan.
            
            User's Primary Problem: {self.user_context.get('problem', 'General life optimization')}
            
            Domain Insights:
            
            HEALTH ANALYSIS:
            {health_output}
            
            FINANCE ANALYSIS:
            {finance_output}
            
            STUDY ANALYSIS:
            {study_output}
            
            Your Coordination Task:
            1. Identify conflicts between domain recommendations
            2. Make trade-off decisions when necessary
            3. Create a unified weekly schedule
            4. Prioritize actions based on urgency/importance
            5. Provide specific cross-domain insights (e.g., "Because stress is high, reduce study hours")
            6. Create a "LifeOps Priority Matrix"
            
            Focus on creating a balanced, sustainable approach that considers:
            - Short-term needs vs long-term goals
            - Resource constraints (time, money, energy)
            - Synergies between domains
            
            Your output must include clear cross-domain reasoning.
            """,
            agent=coordinator,
            expected_output="""A comprehensive life coordination plan with:
            1. Cross-Domain Insights & Reasoning
            2. Priority Matrix (Urgent/Important)
            3. Unified Weekly Schedule
            4. Trade-off Decisions Made
            5. Specific Action Items for Each Domain
            6. Success Metrics & Progress Tracking
            """,
            context=[health_output, finance_output, study_output]
        )