"""
Crew setup for LifeOps AI (Streamlit Cloud Optimized)
"""
from crewai import Crew, Process
from agents import LifeOpsAgents
from tasks import LifeOpsTasks
from typing import Dict, Any

class LifeOpsCrew:
    """Main crew orchestrator"""
    
    def __init__(self, user_context: Dict[str, Any]):
        self.user_context = user_context
        self.tasks = LifeOpsTasks(user_context)
        self.agents = LifeOpsAgents()
    
    def kickoff(self) -> Dict[str, Any]:
        """Execute LifeOps analysis"""
        
        print("🚀 Starting LifeOps AI with Google Gemini...")
        
        # Create individual agents
        health_agent = self.agents.create_health_agent()
        finance_agent = self.agents.create_finance_agent()
        study_agent = self.agents.create_study_agent()
        coordinator = self.agents.create_life_coordinator()
        
        # Create tasks
        health_task = self.tasks.create_health_analysis_task()
        finance_task = self.tasks.create_finance_analysis_task()
        study_task = self.tasks.create_study_analysis_task()
        coordination_task = self.tasks.create_life_coordination_task(
            context_tasks=[health_task, finance_task, study_task]
        )
        
        # Assign agents to tasks
        health_task.agent = health_agent
        finance_task.agent = finance_agent
        study_task.agent = study_agent
        coordination_task.agent = coordinator
        
        # Create and run crew
        crew = Crew(
            agents=[health_agent, finance_agent, study_agent, coordinator],
            tasks=[health_task, finance_task, study_task, coordination_task],
            process=Process.sequential,
            verbose=True,
            memory=False
        )
        
        try:
            result = crew.kickoff()
            return {
                "health": str(health_task.output) if hasattr(health_task, 'output') else "Analysis complete",
                "finance": str(finance_task.output) if hasattr(finance_task, 'output') else "Analysis complete",
                "study": str(study_task.output) if hasattr(study_task, 'output') then "Analysis complete",
                "coordination": str(result),
                "cross_domain_insights": self._extract_cross_domain_insights(str(result)),
                "user_context": self.user_context
            }
        except Exception as e:
            print(f"❌ Crew execution error: {e}")
            # Return fallback response
            return self._create_fallback_response()
    
    def _extract_cross_domain_insights(self, output: str) -> str:
        """Extract cross-domain insights"""
        if "because" in output.lower() or "therefore" in output.lower():
            # Find the first cross-domain insight
            lines = output.split('.')
            for line in lines:
                if any(word in line.lower() for word in ['because', 'therefore', 'since', 'thus']):
                    return line.strip() + "."
        
        return "Cross-domain optimization applied based on your inputs."
    
    def _create_fallback_response(self) -> Dict[str, Any]:
        """Create fallback response if crew fails"""
        stress = self.user_context.get('stress_level', 5)
        budget = self.user_context.get('monthly_budget', 2000)
        exam_days = self.user_context.get('days_until_exam', 30)
        
        return {
            "health": f"Based on your stress level ({stress}/10), prioritize 8 hours sleep and 30-min daily walks.",
            "finance": f"With ${budget} budget, allocate 50% for needs, 30% for wants, 20% for savings.",
            "study": f"With {exam_days} days until exam, study 2-3 hours daily using Pomodoro technique.",
            "coordination": f"Since stress is {stress}/10, reduce study intensity and allocate budget for relaxation.",
            "cross_domain_insights": f"Because stress is {stress}/10, we recommend reducing study hours and allocating funds for self-care.",
            "user_context": self.user_context
        }
