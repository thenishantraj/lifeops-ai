"""
LifeOps AI - Streamlit Application
"""
import streamlit as st
import os
import sys
from datetime import datetime, timedelta
import json

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils import (
    load_env, format_date, calculate_days_until,
    create_health_chart, create_finance_chart, create_study_schedule,
    create_insight_card, parse_agent_output
)
from crew_setup import LifeOpsCrew

# Page configuration
st.set_page_config(
    page_title="LifeOps AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 10px;
        font-weight: 600;
        width: 100%;
        transition: transform 0.2s;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    .agent-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border-left: 4px solid;
    }
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
    }
    .insight-highlight {
        background: linear-gradient(135deg, #667eea20 0%, #764ba220 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None
    if 'user_inputs' not in st.session_state:
        st.session_state.user_inputs = {}
    if 'processing' not in st.session_state:
        st.session_state.processing = False

def main():
    """Main application function"""
    
    # Initialize session state
    initialize_session_state()
    
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown('<h1 class="main-header">🧠 LifeOps AI</h1>', unsafe_allow_html=True)
        st.markdown('<p class="sub-header">Your Personal Life Manager - Integrating Health, Finance & Study</p>', unsafe_allow_html=True)
    
    with col2:
        st.image("https://cdn-icons-png.flaticon.com/512/1998/1998678.png", width=100)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Life Configuration")
        
        # User Inputs
        st.markdown("#### 📊 Current Status")
        
        stress_level = st.slider(
            "Current Stress Level (1-10)",
            min_value=1,
            max_value=10,
            value=5,
            help="1 = Very Relaxed, 10 = Extremely Stressed"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            sleep_hours = st.number_input(
                "Sleep Hours",
                min_value=0,
                max_value=12,
                value=7,
                step=1
            )
        with col2:
            exercise_frequency = st.selectbox(
                "Exercise Frequency",
                ["Rarely", "1-2 times/week", "3-4 times/week", "Daily"]
            )
        
        st.markdown("#### 📚 Study")
        
        exam_date = st.date_input(
            "Upcoming Exam Date",
            min_value=datetime.now(),
            value=datetime.now() + timedelta(days=30)
        )
        
        current_study_hours = st.number_input(
            "Current Daily Study Hours",
            min_value=0,
            max_value=12,
            value=3,
            step=1
        )
        
        st.markdown("#### 💰 Finance")
        
        monthly_budget = st.number_input(
            "Monthly Budget ($)",
            min_value=0,
            value=2000,
            step=100
        )
        
        current_expenses = st.number_input(
            "Current Monthly Expenses ($)",
            min_value=0,
            value=1500,
            step=100
        )
        
        financial_goals = st.text_area(
            "Financial Goals",
            "Save for emergency fund, reduce unnecessary expenses"
        )
        
        # Problem input
        st.markdown("#### 🎯 What's Your Challenge?")
        problem = st.text_area(
            "Describe your current life challenge",
            "I'm stressed about my upcoming exam but also need to manage my budget and health",
            height=100
        )
        
        # Run button
        st.markdown("---")
        run_clicked = st.button(
            "🚀 Run LifeOps Analysis",
            type="primary",
            use_container_width=True
        )
        
        # Store inputs
        user_inputs = {
            'stress_level': stress_level,
            'sleep_hours': sleep_hours,
            'exercise_frequency': exercise_frequency,
            'exam_date': exam_date.strftime("%Y-%m-%d"),
            'days_until_exam': (exam_date - datetime.now().date()).days,
            'current_study_hours': current_study_hours,
            'monthly_budget': monthly_budget,
            'current_expenses': current_expenses,
            'financial_goals': financial_goals,
            'problem': problem
        }
        
        st.session_state.user_inputs = user_inputs
    
    # Main content area
    tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "🤖 AI Analysis", "📅 Action Plan"])
    
    with tab1:
        # Dashboard
        st.markdown("## 📊 Life Dashboard")
        
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="color: #667eea;">{stress_level}/10</h3>
                <p style="color: #666;">Stress Level</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            days_left = calculate_days_until(user_inputs['exam_date'])
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="color: #764ba2;">{days_left}</h3>
                <p style="color: #666;">Days Until Exam</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            savings = monthly_budget - current_expenses
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="color: #4CAF50;">${savings}</h3>
                <p style="color: #666;">Monthly Savings</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            health_score = max(0, 10 - stress_level + (sleep_hours - 5))
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="color: #FF9800;">{int(health_score)}/10</h3>
                <p style="color: #666;">Health Score</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(
                create_health_chart(stress_level, sleep_hours),
                use_container_width=True
            )
        
        with col2:
            st.plotly_chart(
                create_finance_chart(monthly_budget, current_expenses),
                use_container_width=True
            )
        
        # Study Schedule
        st.plotly_chart(
            create_study_schedule(
                user_inputs['days_until_exam'],
                current_study_hours
            ),
            use_container_width=True
        )
    
    with tab2:
        # AI Analysis Area
        st.markdown("## 🤖 AI Life Analysis")
        
        if run_clicked and not st.session_state.processing:
            # Run analysis
            with st.spinner("🧠 LifeOps AI is analyzing your life domains..."):
                try:
                    # Load environment
                    load_env()
                    
                    # Run analysis
                    st.session_state.processing = True
                    
                    # Create and run crew
                    crew = LifeOpsCrew(user_inputs)
                    results = crew.kickoff()
                    
                    # Store results
                    st.session_state.analysis_results = results
                    st.session_state.processing = False
                    
                    # Show success message
                    st.success("✅ LifeOps analysis complete!")
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    st.session_state.processing = False
        
        # Display results if available
        if st.session_state.analysis_results:
            results = st.session_state.analysis_results
            
            # Cross-domain insights highlight
            st.markdown("### 🔄 Cross-Domain Insights")
            st.markdown(f"""
            <div class="insight-highlight">
                <p style="font-size: 1.1rem; font-weight: 500;">
                    {results.get('cross_domain_insights', 'No cross-domain insights extracted.')}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Agent outputs in expandable sections
            st.markdown("### 📋 Domain Analysis")
            
            # Health Analysis
            with st.expander("🏥 Health Analysis", expanded=True):
                st.markdown(create_insight_card(
                    "Health & Wellness Recommendations",
                    results['health'],
                    "Health",
                    "#4CAF50"
                ), unsafe_allow_html=True)
            
            # Finance Analysis
            with st.expander("💰 Finance Analysis", expanded=True):
                st.markdown(create_insight_card(
                    "Financial Planning & Budgeting",
                    results['finance'],
                    "Finance",
                    "#FF9800"
                ), unsafe_allow_html=True)
            
            # Study Analysis
            with st.expander("📚 Study Analysis", expanded=True):
                st.markdown(create_insight_card(
                    "Learning & Productivity Strategy",
                    results['study'],
                    "Study",
                    "#2196F3"
                ), unsafe_allow_html=True)
            
            # Coordination Results
            st.markdown("### 🎯 Integrated Life Plan")
            st.markdown(results['coordination'])
        
        elif not run_clicked:
            st.info("👈 Configure your life settings in the sidebar and click 'Run LifeOps Analysis' to begin.")
    
    with tab3:
        # Action Plan
        st.markdown("## 📅 Your Action Plan")
        
        if st.session_state.analysis_results:
            results = st.session_state.analysis_results
            
            # Create a structured action plan
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("### 🏥 Health Actions")
                st.markdown("""
                - **Today**: Take 3 deep breaths whenever stressed
                - **This Week**: Aim for 7-8 hours of sleep nightly
                - **Ongoing**: 30-minute walk daily
                """)
                
                if st.session_state.user_inputs['stress_level'] > 7:
                    st.warning("⚠️ High stress detected! Consider meditation or short breaks.")
            
            with col2:
                st.markdown("### 📚 Study Actions")
                days_left = st.session_state.user_inputs['days_until_exam']
                study_hours = st.session_state.user_inputs['current_study_hours']
                
                recommended_hours = study_hours
                if st.session_state.user_inputs['stress_level'] > 7:
                    recommended_hours = max(1, study_hours - 2)
                    st.info(f"📉 Reduced study hours to {recommended_hours}/day due to high stress")
                
                st.markdown(f"""
                - **Schedule**: {recommended_hours} hours/day focused study
                - **Technique**: Pomodoro (25 min study, 5 min break)
                - **Weekly Goal**: Cover 3 main topics
                """)
            
            with col3:
                st.markdown("### 💰 Finance Actions")
                budget = st.session_state.user_inputs['monthly_budget']
                expenses = st.session_state.user_inputs['current_expenses']
                
                st.markdown(f"""
                - **Budget**: ${budget - expenses} for savings this month
                - **Review**: Check subscription services
                - **Plan**: Allocate funds for health/study needs
                """)
            
            # Weekly Schedule
            st.markdown("### 🗓️ Suggested Weekly Schedule")
            
            # Create a sample weekly schedule based on inputs
            schedule_data = {
                "Time": ["Morning", "Afternoon", "Evening", "Night"],
                "Monday": ["Exercise", "Study", "Work/Break", "Relax"],
                "Tuesday": ["Study", "Health Check", "Budget Review", "Sleep"],
                "Wednesday": ["Exercise", "Deep Work", "Social", "Wind Down"],
                "Thursday": ["Study", "Break", "Exercise", "Plan Next Day"],
                "Friday": ["Review Week", "Light Study", "Fun", "Sleep Early"],
                "Saturday": ["Rest", "Hobby", "Outdoor", "Social"],
                "Sunday": ["Plan Week", "Prep", "Relax", "Early Sleep"]
            }
            
            st.dataframe(schedule_data, use_container_width=True)
            
            # Download button for action plan
            action_plan = {
                "user_context": st.session_state.user_inputs,
                "health_recommendations": results['health'][:500] + "...",
                "finance_recommendations": results['finance'][:500] + "...",
                "study_recommendations": results['study'][:500] + "...",
                "integrated_plan": results['coordination'][:1000] + "..."
            }
            
            st.download_button(
                label="📥 Download Action Plan",
                data=json.dumps(action_plan, indent=2),
                file_name="lifeops_action_plan.json",
                mime="application/json"
            )
        
        else:
            st.info("Run the analysis first to see your personalized action plan.")

if __name__ == "__main__":
    main()