# Autonomous Quote Agent Intelligence Platform

## Overview
The Autonomous Quote Agent Intelligence Platform is a multi-agent AI system designed to automate the auto insurance quote lifecycle.
The platform processes insurance quotes using a pipeline of AI agents that analyze risk, predict conversion probability, recommend premiums, and route final decisions automatically.
This project was developed during a hackathon to demonstrate how Agentic AI systems can automate insurance workflows and reduce manual intervention.

## Problem Statement
Auto insurance companies generate thousands of quotes daily, but only a small percentage convert into actual policies.
Many quotes expire because manual investigation is required to understand:

- Why the quote did not convert
- Whether the premium was appropriate
- Whether the agent should follow up

This project builds an autonomous AI pipeline that analyzes quotes, predicts conversion probability, recommends optimal premiums, and routes decisions automatically.


## Solution
Our solution introduces autonomous AI agents that process insurance quotes automatically through a multi-agent pipeline.

The system includes four specialized AI agents:

- Risk Profiler – Analyzes driver and vehicle risk factors  
- Conversion Predictor – Predicts probability of policy conversion  
- Premium Advisor – Recommends optimal premium pricing  
- Decision Router – Determines the final action (Auto bind / Follow-up / Escalation)


## System Architecture
The platform follows a sequential multi-agent pipeline:

User Input  
↓  
Frontend Dashboard  
↓  
FastAPI Backend  
↓  
Risk Profiler  
↓  
Conversion Predictor  
↓  
Premium Advisor  
↓  
Decision Router  
↓  
Final Decision Returned  


## Tech Stack

### Frontend
- HTML
- JavaScript
- CSS
- Fetch API

### Backend
- Python
- FastAPI
- Machine Learning Models
- Pandas

### Tools
- GitHub
- VS Code


## Project Structure


hackathon
│
├── backend
│ ├── app
│ │ ├── routers
│ │ ├── services
│ │ └── main.py
│
└── frontend
├── index.html
└── script.js



## Features
✔ Multi-agent AI pipeline  
✔ Automated insurance quote analysis  
✔ Risk profiling system  
✔ Conversion prediction model  
✔ Premium recommendation engine  
✔ Decision routing automation  
✔ Real-time dashboard interface  


## How to Run the Project

### 1. Clone the Repository

git clone https://github.com/your-repo.git

cd hackathon


### 2. Run the Backend

cd backend/app
uvicorn main:app --reload


Backend will run at:

http://127.0.0.1:8000

API documentation:

http://127.0.0.1:8000/docs


### 3. Run the Frontend
Open the frontend file:


frontend/index.html


Or run it using Live Server in VS Code.


## Team
Developed during the Hackathon by our team.


## Future Improvements
- Add explainability using SHAP/LIME
- Integrate real insurance datasets
- Deploy system using Docker and cloud infrastructure
- Add analytics dashboards for insurance agents