"""
Utility functions for LifeOps AI
"""
import os
import json
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import streamlit as st

def load_env() -> str:
    """Load environment variables - Streamlit Cloud compatible"""
    # Check if running on Streamlit Cloud
    if 'GOOGLE_API_KEY' in os.environ:
        api_key = os.environ["GOOGLE_API_KEY"]
    else:
        # Try to load from .env locally
        try:
            from dotenv import load_dotenv
            load_dotenv()
            api_key = os.getenv("GOOGLE_API_KEY")
        except ImportError:
            api_key = None
    
    # Debug info
    if api_key:
        key_start = api_key[:10] if len(api_key) > 10 else api_key
        print(f"🔑 API Key loaded (starts with): {key_start}...")
        
        # Check if it's still the placeholder
        if api_key == "your_google_api_key_here" or api_key == "NA":
            st.warning("⚠️ Please replace the placeholder API key with your actual Google Gemini API key")
    
    if not api_key or api_key in ["your_google_api_key_here", "NA", ""]:
        raise ValueError("""
        GOOGLE_API_KEY not found or invalid.
        
        Please add your Google Gemini API key:
        
        For Streamlit Cloud:
        1. Go to: https://share.streamlit.io/
        2. Select your app → Settings → Secrets
        3. Add: GOOGLE_API_KEY = "your_actual_key_here"
        
        For Local Development:
        1. Create .streamlit/secrets.toml
        2. Add: GOOGLE_API_KEY = "your_actual_key_here"
        
        Get your free key from: https://makersuite.google.com/app/apikey
        """)
    
    return api_key

def format_date(date_str: str) -> str:
    """Format date for display"""
    try:
        if isinstance(date_str, str):
            date = datetime.strptime(date_str, "%Y-%m-%d")
        else:
            date = date_str
        return date.strftime("%B %d, %Y")
    except Exception:
        return str(date_str)

def calculate_days_until(target_date: str) -> int:
    """Calculate days until a target date"""
    try:
        if isinstance(target_date, str):
            target = datetime.strptime(target_date, "%Y-%m-%d")
        else:
            target = target_date
        today = datetime.now()
        days = (target - today).days
        return max(0, days)  # Don't show negative days
    except Exception:
        return 30  # Default to 30 days

def create_health_chart(stress_level: int, hours_sleep: int = 7, exercise_minutes: int = 30) -> go.Figure:
    """Create a health dashboard chart"""
    fig = go.Figure()
    
    # Stress level gauge
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=stress_level,
        title={'text': "Stress Level", 'font': {'size': 18}},
        domain={'row': 0, 'column': 0},
        gauge={
            'axis': {'range': [0, 10], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 3], 'color': "#4CAF50"},  # Green
                {'range': [3, 7], 'color': "#FFC107"},  # Yellow
                {'range': [7, 10], 'color': "#F44336"}  # Red
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 7
            }
        }
    ))
    
    # Add sleep and exercise indicators as annotations
    fig.add_annotation(
        x=0.5, y=0.2,
        text=f"Sleep: {hours_sleep}h | Exercise: {exercise_minutes}min",
        showarrow=False,
        font=dict(size=14, color="gray")
    )
    
    fig.update_layout(
        height=300,
        margin=dict(t=50, b=30, l=30, r=30),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    
    return fig

def create_finance_chart(budget: float, expenses: float = 0) -> go.Figure:
    """Create a finance chart"""
    expenses = min(expenses, budget)  # Ensure expenses don't exceed budget
    savings = max(0, budget - expenses)
    
    # Create data
    categories = ['Essential Expenses', 'Discretionary Spending', 'Savings']
    
    # Calculate allocations (50% essentials, 30% discretionary, 20% savings as ideal)
    essential_recommended = budget * 0.5
    discretionary_recommended = budget * 0.3
    savings_recommended = budget * 0.2
    
    # Current vs Recommended
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Current',
        x=categories,
        y=[expenses * 0.7, expenses * 0.3, savings],
        marker_color=['#2E86AB', '#A23B72', '#F18F01'],
        text=[f"${expenses*0.7:.0f}", f"${expenses*0.3:.0f}", f"${savings:.0f}"],
        textposition='auto',
    ))
    
    fig.add_trace(go.Bar(
        name='Recommended',
        x=categories,
        y=[essential_recommended, discretionary_recommended, savings_recommended],
        marker_color=['rgba(46, 134, 171, 0.3)', 'rgba(162, 59, 114, 0.3)', 'rgba(241, 143, 1, 0.3)'],
        text=[f"${essential_recommended:.0f}", f"${discretionary_recommended:.0f}", f"${savings_recommended:.0f}"],
        textposition='auto',
    ))
    
    fig.update_layout(
        title="Budget Allocation (Current vs Recommended)",
        barmode='group',
        height=300,
        xaxis_title="Category",
        yaxis_title="Amount ($)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(t=50, b=30, l=30, r=30),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    
    return fig

def create_study_schedule(days_until_exam: int, study_hours_per_day: int) -> go.Figure:
    """Create a study schedule timeline"""
    if days_until_exam <= 0:
        days_until_exam = 7  # Default to one week
    
    # Adjust study hours based on days until exam
    if days_until_exam < 7:
        # Intensive study for last week
        base_hours = min(8, study_hours_per_day * 1.5)
    elif days_until_exam < 14:
        # Moderate study for 2 weeks
        base_hours = study_hours_per_day
    else:
        # Relaxed study for longer periods
        base_hours = max(2, study_hours_per_day * 0.8)
    
    dates = []
    hours = []
    colors = []
    
    today = datetime.now()
    
    for i in range(min(days_until_exam, 14)):  # Show max 14 days
        date = today + timedelta(days=i)
        dates.append(date.strftime("%b %d"))
        
        # Taper study hours as exam approaches
        if i == 0:
            # Today
            hour = base_hours
            colors.append('#2E86AB')  # Blue for today
        elif i == days_until_exam - 1:
            # Day before exam
            hour = max(1, base_hours * 0.3)  # Light review
            colors.append('#F18F01')  # Orange for exam day
        elif i >= days_until_exam - 3:
            # Last 3 days (excluding exam day)
            hour = base_hours * 0.7
            colors.append('#A23B72')  # Purple for last days
        else:
            # Regular study days
            hour = base_hours
            colors.append('#2E86AB')  # Blue for regular days
        
        hours.append(round(hour, 1))
    
    fig = go.Figure(data=[go.Bar(
        x=dates,
        y=hours,
        marker_color=colors,
        text=hours,
        textposition='auto',
        hovertemplate='<b>%{x}</b><br>Study Hours: %{y}<extra></extra>'
    )])
    
    # Add exam day marker
    if days_until_exam <= 14:
        fig.add_vline(
            x=days_until_exam - 1,
            line_width=2,
            line_dash="dash",
            line_color="red",
            annotation_text="Exam Day",
            annotation_position="top"
        )
    
    fig.update_layout(
        title=f"Study Schedule (Next {len(dates)} Days)",
        xaxis_title="Date",
        yaxis_title="Study Hours",
        height=300,
        margin=dict(t=50, b=30, l=30, r=30),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    
    return fig

def create_insight_card(title: str, content: str, agent: str, color: str = "#2E86AB") -> str:
    """Create a formatted insight card"""
    agent_colors = {
        "Health": "#4CAF50",
        "Finance": "#FF9800",
        "Study": "#2196F3",
        "Coordinator": "#9C27B0"
    }
    
    card_color = agent_colors.get(agent, color)
    
    # Clean up content for HTML
    content = str(content).replace('\n', '<br>')
    
    card = f"""
    <div style="
        background: linear-gradient(135deg, {card_color}10, {card_color}05);
        border-left: 4px solid {card_color};
        padding: 20px;
        border-radius: 10px;
        margin: 15px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        transition: transform 0.2s, box-shadow 0.2s;
    "
    onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 6px 12px rgba(0,0,0,0.1)'"
    onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 6px rgba(0,0,0,0.05)'"
    >
        <div style="display: flex; align-items: center; margin-bottom: 15px;">
            <div style="
                width: 40px;
                height: 40px;
                background-color: {card_color};
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                margin-right: 15px;
                color: white;
                font-weight: bold;
                font-size: 18px;
            ">
                {agent[0]}
            </div>
            <div>
                <h4 style="margin: 0; color: {card_color}; font-weight: 600; font-size: 1.2rem;">{title}</h4>
                <p style="margin: 5px 0 0 0; color: #666; font-size: 0.9rem;">{agent} Agent</p>
            </div>
        </div>
        <div style="
            padding: 15px;
            background: white;
            border-radius: 8px;
            border: 1px solid rgba(0,0,0,0.05);
        ">
            <p style="margin: 0; color: #333; line-height: 1.6; font-size: 0.95rem;">{content}</p>
        </div>
        <div style="
            margin-top: 15px;
            padding-top: 10px;
            border-top: 1px solid rgba(0,0,0,0.1);
            font-size: 0.8em;
            color: #666;
            display: flex;
            align-items: center;
            justify-content: space-between;
        ">
            <span>📊 <strong>Agent:</strong> {agent}</span>
            <span style="
                background: {card_color}20;
                color: {card_color};
                padding: 3px 10px;
                border-radius: 12px;
                font-size: 0.75em;
                font-weight: 600;
            ">
                AI Analysis
            </span>
        </div>
    </div>
    """
    
    return card

def parse_agent_output(output: str) -> Dict[str, Any]:
    """Parse agent output into structured data"""
    try:
        if not output:
            return {"raw_output": "No output received"}
        
        output_str = str(output)
        
        # Try to extract JSON-like content
        json_str = None
        
        if "```json" in output_str:
            parts = output_str.split("```json")
            if len(parts) > 1:
                json_str = parts[1].split("```")[0].strip()
        elif "```" in output_str:
            parts = output_str.split("```")
            if len(parts) > 1:
                potential_json = parts[1].strip()
                if potential_json.startswith("json"):
                    json_str = potential_json[4:].strip()
                elif potential_json.startswith("{"):
                    json_str = potential_json
        else:
            # Look for JSON-like structure
            start_idx = output_str.find("{")
            end_idx = output_str.rfind("}")
            if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
                json_str = output_str[start_idx:end_idx+1]
        
        if json_str:
            try:
                parsed = json.loads(json_str)
                if isinstance(parsed, dict):
                    return parsed
            except json.JSONDecodeError:
                # Try to fix common JSON issues
                json_str = json_str.replace("'", '"').replace("None", "null").replace("True", "true").replace("False", "false")
                try:
                    parsed = json.loads(json_str)
                    if isinstance(parsed, dict):
                        return parsed
                except:
                    pass
        
        # If no JSON found, return structured analysis
        return {
            "analysis": output_str[:500] + ("..." if len(output_str) > 500 else ""),
            "raw_output": output_str,
            "summary": output_str[:200].split('.')[0] + "."
        }
        
    except Exception as e:
        print(f"Error parsing agent output: {e}")
        return {
            "raw_output": str(output)[:1000],
            "error": f"Parse error: {str(e)}",
            "summary": "Agent analysis completed successfully."
        }

def create_progress_chart(completed: int, total: int, title: str = "Progress") -> go.Figure:
    """Create a progress chart"""
    percentage = (completed / total * 100) if total > 0 else 0
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=percentage,
        title={'text': title, 'font': {'size': 16}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1},
            'bar': {'color': "#4CAF50"},
            'steps': [
                {'range': [0, 33], 'color': "#F44336"},
                {'range': [33, 66], 'color': "#FFC107"},
                {'range': [66, 100], 'color': "#4CAF50"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 80
            }
        }
    ))
    
    fig.update_layout(
        height=200,
        margin=dict(t=30, b=10, l=30, r=30)
    )
    
    return fig

def calculate_life_balance_score(
    stress_level: int,
    sleep_hours: int,
    budget_ratio: float,
    study_balance: float
) -> int:
    """Calculate overall life balance score (0-100)"""
    # Normalize inputs
    stress_score = max(0, 100 - (stress_level * 10))  # 0-100, lower stress = higher score
    
    sleep_score = 0
    if sleep_hours >= 7 and sleep_hours <= 9:
        sleep_score = 100  # Optimal sleep
    elif sleep_hours >= 6 and sleep_hours <= 10:
        sleep_score = 70   # Acceptable sleep
    else:
        sleep_score = 30   # Poor sleep
    
    # Budget ratio = savings / income (ideal is 0.2 or 20%)
    budget_score = min(100, budget_ratio * 500)  # 0-100, higher savings = higher score
    
    # Study balance = study hours / available time (ideal is 0.3 or 30%)
    study_score = 100 - abs(study_balance - 0.3) * 300  # Penalize deviation from 30%
    study_score = max(0, min(100, study_score))
    
    # Weighted average
    total_score = (
        stress_score * 0.3 +      # Stress is most important
        sleep_score * 0.25 +      # Sleep is very important
        budget_score * 0.25 +     # Financial health is important
        study_score * 0.2         # Study balance is important
    )
    
    return int(total_score)

def format_currency(amount: float) -> str:
    """Format currency for display"""
    if amount >= 1000:
        return f"${amount:,.0f}"
    else:
        return f"${amount:,.2f}"

def get_time_of_day_greeting() -> str:
    """Get appropriate greeting based on time of day"""
    hour = datetime.now().hour
    
    if hour < 12:
        return "Good morning! ☀️"
    elif hour < 17:
        return "Good afternoon! 🌤️"
    elif hour < 21:
        return "Good evening! 🌙"
    else:
        return "Good night! 🌟"

def create_recommendation_bullets(recommendations: list, limit: int = 5) -> str:
    """Create formatted recommendation bullets"""
    if not recommendations:
        return "No specific recommendations available."
    
    bullets = ""
    for i, rec in enumerate(recommendations[:limit]):
        emoji = "✅" if i == 0 else "•"
        bullets += f"{emoji} {rec}<br>"
    
    return bullets

def validate_user_inputs(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """Validate and sanitize user inputs"""
    validated = {}
    
    for key, value in inputs.items():
        if value is None:
            validated[key] = ""
        elif isinstance(value, (int, float)):
            # Ensure numeric values are within reasonable ranges
            if key == 'stress_level':
                validated[key] = max(1, min(10, value))
            elif key in ['sleep_hours', 'current_study_hours']:
                validated[key] = max(0, min(24, value))
            elif key in ['monthly_budget', 'current_expenses']:
                validated[key] = max(0, min(1000000, value))
            else:
                validated[key] = value
        else:
            validated[key] = str(value)
    
    return validated
