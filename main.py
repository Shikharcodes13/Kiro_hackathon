from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uvicorn

from app.orchestrator.task_manager import TaskManager
from app.models.schemas import QueryRequest, AgentResponse

app = FastAPI(
    title="AutoAgent - Agentic Automotive Platform",
    description="Multi-agent system for automotive industry with specialized AI agents",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize task manager
task_manager = TaskManager()

@app.get("/")
async def root():
    return {
        "message": "🚗 AutoAgent Platform - Agentic Automotive Intelligence",
        "version": "1.0.0",
        "agents": [
            "🤝 Buyer Agent",
            "💸 Seller Agent", 
            "🛠️ Owner Agent",
            "📑 Document Agent",
            "📊 Dealer Agent",
            "🧠 RAG Agent",
            "💰 Loan Agent"
        ]
    }

@app.post("/query", response_model=AgentResponse)
async def process_query(request: QueryRequest):
    """
    Main endpoint for processing user queries through the agent orchestration system
    """
    try:
        result = await task_manager.orchestrate_task(
            user_query=request.query,
            context=request.context or {}
        )
        
        return AgentResponse(
            session_id=result["session_id"],
            result=result["result"],
            agent_trace=result["agent_trace"],
            success=True
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent processing failed: {str(e)}")

@app.get("/demo")
async def demo_flow():
    """
    Hackathon demo endpoint - showcases the 3-minute agent collaboration flow
    """
    demo_query = "Best EV under ₹15L in Delhi?"
    
    result = await task_manager.orchestrate_task(
        user_query=demo_query,
        context={"demo_mode": True}
    )
    
    return {
        "demo_scenario": "🎯 Hackathon Demo: EV Car Search",
        "user_query": demo_query,
        "agent_collaboration": result["agent_trace"],
        "final_result": result["result"],
        "execution_time": "< 3 seconds",
        "agents_involved": len(result["agent_trace"])
    }

@app.get("/agents")
async def list_agents():
    """
    List all available agents and their capabilities
    """
    return {
        "agents": task_manager.get_agent_capabilities(),
        "total_agents": len(task_manager.get_agent_capabilities())
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "agents": "operational"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)