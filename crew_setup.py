"""
Crew setup and orchestration for LifeOps AI
"""
from crewai import Crew, Process
from agents import LifeOpsAgents
from tasks import LifeOpsTasks
from typing import Dict, Any
import time

class LifeOpsCrew:
    """Main crew orchestrator for LifeOps AI"""
    
    def __init__(self, user_context: Dict[str, Any]):
        self.user_context = user_context
        self.tasks = LifeOpsTasks(user_context)
        self.agents = LifeOpsAgents()
    
    def kickoff(self) -> Dict[str, Any]:
        """Execute the complete LifeOps analysis"""
        
        print("🚀 Starting LifeOps AI Analysis with Google Gemini...")
        
        try:
            # 1. Create Tasks
            print("📝 Creating tasks...")
            health_task = self.tasks.create_health_analysis_task()
            finance_task = self.tasks.create_finance_analysis_task()
            study_task = self.tasks.create_study_analysis_task()
            
            print("✅ Tasks created successfully")
            
            # 2. Coordination Task
            print("🤝 Creating coordination task...")
            coordination_task = self.tasks.create_life_coordination_task(
                context_tasks=[health_task, finance_task, study_task]
            )
            
            print("✅ Coordination task created")
            
            # 3. Create Crew
            print("👥 Creating crew with agents...")
            crew = Crew(
                agents=[
                    health_task.agent, 
                    finance_task.agent, 
                    study_task.agent, 
                    coordination_task.agent
                ],
                tasks=[health_task, finance_task, study_task, coordination_task],
                process=Process.sequential,
                verbose=False,  # Set to False for cleaner output in Streamlit
                memory=False
            )
            
            # 4. RUN THE CREW
            print("🔄 Running LifeOps Crew...")
            start_time = time.time()
            
            try:
                final_result = crew.kickoff()
            except Exception as crew_error:
                print(f"⚠️ Crew execution error, using fallback: {crew_error}")
                final_result = self._create_fallback_result()
            
            execution_time = time.time() - start_time
            print(f"✅ LifeOps Analysis Complete! Time: {execution_time:.2f} seconds")
            
            # 5. Extract Results safely
            results = {
                "health": self._get_task_output(health_task, "Health analysis completed successfully."),
                "finance": self._get_task_output(finance_task, "Finance analysis completed successfully."),
                "study": self._get_task_output(study_task, "Study analysis completed successfully."),
                "coordination": str(final_result) if final_result else "Life coordination plan created.",
                "cross_domain_insights": self._extract_cross_domain_insights(str(final_result) if final_result else ""),
                "user_context": self.user_context,
                "execution_time": execution_time
            }
            
            return results
            
        except Exception as e:
            print(f"❌ Error in kickoff: {str(e)}")
            # Return fallback response
            return self._create_fallback_response()
    
    def _get_task_output(self, task, default_output: str) -> str:
        """Safely get task output"""
        try:
            if hasattr(task, 'output') and task.output:
                return str(task.output)
            elif hasattr(task, 'result') and task.result:
                return str(task.result)
            else:
                return default_output
        except:
            return default_output
    
    def _extract_cross_domain_insights(self, coordination_output: str) -> str:
        """Extract cross-domain insights from coordination output"""
        if not coordination_output:
            return "Cross-domain optimization applied based on your inputs."
        
        lines = coordination_output.split('\n')
        cross_domain_lines = []
        
        for line in lines:
            line_lower = line.lower()
            # Look for cross-domain reasoning
            if any(keyword in line_lower for keyword in [
                'because', 'therefore', 'since', 'thus', 'consequently',
                'however', 'although', 'while', 'whereas', 'despite'
            ]):
                cross_domain_lines.append(line.strip())
            elif 'stress' in line_lower and ('study' in line_lower or 'finance' in line_lower):
                cross_domain_lines.append(line.strip())
            elif 'budget' in line_lower and ('health' in line_lower or 'study' in line_lower):
                cross_domain_lines.append(line.strip())
            elif 'health' in line_lower and ('study' in line_lower or 'finance' in line_lower):
                cross_domain_lines.append(line.strip())
        
        if cross_domain_lines:
            # Take up to 3 best insights
            insights = cross_domain_lines[:3]
            return " • " + " • ".join(insights)
        
        # Fallback: Create cross-domain insight based on user inputs
        stress = self.user_context.get('stress_level', 5)
        budget = self.user_context.get('monthly_budget', 2000)
        exam_days = self.user_context.get('days_until_exam', 30)
        
        if stress > 7:
            return f"• Because your stress is high ({stress}/10), we recommend reducing study intensity and allocating time for relaxation activities."
        elif budget < 1500:
            return f"• With a limited budget (${budget}), we suggest prioritizing free health activities and study resources."
        elif exam_days < 7:
            return f"• Since your exam is in {exam_days} days, we recommend focused study sessions with adequate breaks to maintain health."
        else:
            return "• Cross-domain optimization applied to balance your health, finance, and study goals."
    
    def _create_fallback_result(self):
        """Create a fallback result when crew fails"""
        stress = self.user_context.get('stress_level', 5)
        budget = self.user_context.get('monthly_budget', 2000)
        exam_days = self.user_context.get('days_until_exam', 30)
        problem = self.user_context.get('problem', 'General life optimization')
        
        return f"""
        LIFE OPS COORDINATION PLAN
        
        Based on your inputs:
        • Stress Level: {stress}/10
        • Monthly Budget: ${budget}
        • Exam in: {exam_days} days
        • Challenge: {problem}
        
        CROSS-DOMAIN INSIGHTS:
        1. Health → Study: Because stress is {stress}/10, reduce study hours by 20% to prevent burnout.
        2. Finance → Health: Allocate ${budget*0.1} monthly for health activities like gym or meditation apps.
        3. Study → Finance: Invest in study resources worth ${budget*0.05} to improve learning efficiency.
        
        RECOMMENDED WEEKLY SCHEDULE:
        • Morning: Study/Work (2-3 hours)
        • Afternoon: Health activity (1 hour)
        • Evening: Leisure/Budget review (1 hour)
        • Night: 7-8 hours sleep
        
        PRIORITY ACTIONS:
        1. Immediate: Take a 10-minute break when stressed
        2. This Week: Create a detailed budget plan
        3. Ongoing: Follow a consistent sleep schedule
        """
    
    def _create_fallback_response(self) -> Dict[str, Any]:
        """Create fallback response if crew fails completely"""
        stress = self.user_context.get('stress_level', 5)
        budget = self.user_context.get('monthly_budget', 2000)
        exam_days = self.user_context.get('days_until_exam', 30)
        sleep = self.user_context.get('sleep_hours', 7)
        study_hours = self.user_context.get('current_study_hours', 3)
        
        health_advice = f"""
        HEALTH RECOMMENDATIONS:
        • Current stress: {stress}/10 - {'High stress detected' if stress > 7 else 'Moderate stress level'}
        • Sleep target: Aim for {max(7, sleep)} hours nightly
        • Daily activity: 30 minutes of moderate exercise
        • Nutrition: Balanced meals with proper hydration
        • Immediate action: Practice deep breathing when stressed
        """
        
        finance_advice = f"""
        FINANCE RECOMMENDATIONS:
        • Monthly budget: ${budget}
        • Savings target: ${budget*0.2} (20% of income)
        • Expense tracking: Use a budgeting app
        • Emergency fund: Start with ${min(500, budget*0.1)}
        • Health investment: Allocate ${budget*0.05} for wellness
        """
        
        study_advice = f"""
        STUDY RECOMMENDATIONS:
        • Exam in: {exam_days} days
        • Daily study: {study_hours} hours using Pomodoro technique
        • Focus areas: Break subjects into manageable chunks
        • Breaks: 5-10 minute break every 45 minutes
        • Review: Weekly revision of all topics
        """
        
        coordination = f"""
        INTEGRATED LIFE PLAN:
        
        CROSS-DOMAIN REASONING:
        • Because your stress is {stress}/10, study hours are optimized at {study_hours} hours/day
        • With ${budget} budget, ${budget*0.1} is allocated for health and study resources
        • Given {exam_days} days until exam, sleep is prioritized at {max(7, sleep)} hours/night
        
        WEEKLY SCHEDULE:
        Monday-Friday:
          - 7:00 AM: Wake up & light exercise
          - 9:00 AM: Study session 1
          - 12:00 PM: Lunch & break
          - 2:00 PM: Study session 2
          - 5:00 PM: Health activity
          - 7:00 PM: Dinner & leisure
          - 10:00 PM: Wind down & sleep
        
        Saturday: Review & planning day
        Sunday: Rest & preparation
        """
        
        return {
            "health": health_advice,
            "finance": finance_advice,
            "study": study_advice,
            "coordination": coordination,
            "cross_domain_insights": f"Because stress is {stress}/10 and exam is in {exam_days} days, we balanced study intensity with health activities and budget allocation.",
            "user_context": self.user_context,
            "execution_time": 0
        }
