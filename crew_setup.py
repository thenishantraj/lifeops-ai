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
        
        # Create individual tasks
        health_task = self.tasks.create_health_analysis_task()
        finance_task = self.tasks.create_finance_analysis_task()
        study_task = self.tasks.create_study_analysis_task()
        
        # Execute individual domain tasks
        print("🧠 Analyzing Health Domain...")
        health_result = health_task.execute()
        
        print("💰 Analyzing Finance Domain...")
        finance_result = finance_task.execute()
        
        print("📚 Analyzing Study Domain...")
        study_result = study_task.execute()
        
        # Create and execute coordination task
        coordination_task = self.tasks.create_life_coordination_task(
            health_result,
            finance_result,
            study_result
        )
        
        print("🔄 Coordinating Life Domains...")
        coordination_result = coordination_task.execute()
        
        # Compile results
        results = {
            "health": health_result,
            "finance": finance_result,
            "study": study_result,
            "coordination": coordination_result,
            "cross_domain_insights": self._extract_cross_domain_insights(coordination_result),
            "user_context": self.user_context
        }
        
        print("✅ LifeOps Analysis Complete!")
        return results
    
    def _extract_cross_domain_insights(self, coordination_output: str) -> str:
        """Extract cross-domain insights from coordination output"""
        # This is a simplified extraction - in production, you might use more sophisticated parsing
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
            return "\n".join(cross_domain_lines[:5])  # Return top 5 insights
        
        # If no explicit cross-domain insights found, return the first paragraph
        paragraphs = coordination_output.split('\n\n')
        return paragraphs[0] if paragraphs else "Cross-domain insights integrated into the plan."
    
    def run_sequential_crew(self):
        """Alternative: Run as a single crew with sequential process"""
        agents = self.agents.get_all_agents()
        
        # Get all tasks
        tasks = [
            self.tasks.create_health_analysis_task(),
            self.tasks.create_finance_analysis_task(),
            self.tasks.create_study_analysis_task(),
        ]
        
        # Add coordination task
        coordination_task = self.tasks.create_life_coordination_task(
            "", "", ""  # Placeholders, will be filled by context
        )
        tasks.append(coordination_task)
        
        # Create crew
        crew = Crew(
            agents=agents,
            tasks=tasks,
            verbose=True,
            process=Process.sequential,
            memory=True,
            cache=True
        )
        
        return crew.kickoff()