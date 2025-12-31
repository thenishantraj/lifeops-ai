
# 🧠 LifeOps AI - Personal Operations Manager

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![CrewAI](https://img.shields.io/badge/Orchestration-CrewAI-orange)
![Gemini](https://img.shields.io/badge/AI-Gemini%201.5%20Flash-green)


**LifeOps AI** is not just a chatbot; it is an **Agentic AI System** designed to be your proactive Personal Operations Manager. Unlike traditional apps that work in silos, LifeOps AI connects **Health**, **Finance**, and **Study** domains to provide holistic, cross-domain life decisions.

---

## 🚀 Key Features

- **🤖 Multi-Agent Architecture:** Powered by **CrewAI**, featuring specialized agents:
  - **🏥 Health Agent:** Tracks stress, sleep, and wellness.
  - **💰 Finance Agent:** Manages budget, expenses, and savings.
  - **📚 Study Agent:** Optimizes learning schedules and prevents burnout.
  - **🧠 Main Brain (Orchestrator):** Coordinates all agents to make trade-off decisions.
  
- **🔄 Cross-Domain Reasoning:** The system understands how one area of life affects another.
  > *Example:* "Because your stress level is high (Health), the system automatically reduces your study load (Study) and suggests a budget-friendly relaxation activity (Finance)."

- **📊 Interactive Dashboard:** A clean, real-time UI built with **Streamlit** to visualize your life metrics.

---

## 🛠️ Tech Stack

- **LLM:** Google Gemini 1.5 Flash (via API)
- **Orchestration:** CrewAI
- **Frontend:** Streamlit
- **Backend:** Python
- **Visualization:** Plotly
- **Environment Management:** Python-Dotenv

---

## 📂 Project Structure

```bash
lifeops-ai/
├── agents.py           # Defines the 4 AI Agents (Health, Finance, Study, Brain)
├── tasks.py            # Defines specific tasks and cross-domain logic
├── app.py              # Main Streamlit Application (UI)
├── crew_setup.py       # Orchestration logic to run the agents
├── utils.py            # Helper functions for charts and data
├── requirements.txt    # List of dependencies
├── .env                # API Keys (Not uploaded to GitHub)
└── README.md           # Documentation
