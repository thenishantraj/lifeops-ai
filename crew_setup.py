"""
Crew setup and orchestration for LifeOps AI
"""
from crewai import Crew, Process
from agents import LifeOpsAgents
from tasks import LifeOpsTasks
from typing import Dict, Any

class LifeOpsCrew:
    """Main crew orchestrator for LifeOps AI"""
    
    def __init__(self, user_context: Dict[str, Any]):
        self.user_context = user_context
        self.tasks = LifeOpsTasks(user_context)
        self.agents = LifeOpsAgents()
    
    def kickoff(self) -> Dict[str, Any]:
        """Execute the complete LifeOps analysis"""
        
        print("🚀 Starting LifeOps AI Analysis...")
        
        # 1. Create Tasks (Task Objects banaye)
        health_task = self.tasks.create_health_analysis_task()
        finance_task = self.tasks.create_finance_analysis_task()
        study_task = self.tasks.create_study_analysis_task()
        
        # 2. Coordination Task (Ab ye list of tasks lega - Corrected)
        coordination_task = self.tasks.create_life_coordination_task(
            context_tasks=[health_task, finance_task, study_task]
        )
        
        # 3. Create Crew (Saare agents aur tasks ko ek team banaya)
        crew = Crew(
            agents=[
                health_task.agent, 
                finance_task.agent, 
                study_task.agent, 
                coordination_task.agent
            ],
            tasks=[health_task, finance_task, study_task, coordination_task],
            process=Process.sequential,
            verbose=True
        )
        
        # 4. RUN THE CREW (Ye ek baar mein sab chalayega)
        print("🔄 Running LifeOps Crew...")
        final_result = crew.kickoff()
        
        # 5. Extract Results safely
        print("✅ LifeOps Analysis Complete!")
        
        return {
            "health": str(health_task.output),
            "finance": str(finance_task.output),
            "study": str(study_task.output),
            "coordination": str(final_result),
            "cross_domain_insights": self._extract_cross_domain_insights(str(final_result)),
            "user_context": self.user_context
        }
    
    def _extract_cross_domain_insights(self, coordination_output: str) -> str:
        """Extract cross-domain insights from coordination output"""
        lines = coordination_output.split('\n')
        cross_domain_lines = []
        
        for line in lines:
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in ['cross-domain', 'because', 'therefore', 'since', 'thus', 'consequently']):
                cross_domain_lines.append(line)
            elif 'stress' in line_lower and ('study' in line_lower or 'finance' in line_lower):
                cross_domain_lines.append(line)
            elif 'budget' in line_lower and ('health' in line_lower or 'study' in line_lower):
                cross_domain_lines.append(line)
        
        if cross_domain_lines:
            return "\n".join(cross_domain_lines[:5])
        
        paragraphs = coordination_output.split('\n\n')
        return paragraphs[0] if paragraphs else "Cross-domain insights integrated into the plan."
