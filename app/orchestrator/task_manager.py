import asyncio
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional
import importlib

from app.models.schemas import AgentTrace

class TaskManager:
    def __init__(self):
        self.task_queue = []
        self.active_agents = {}
        self.agent_traces = {}
        self.event_bus = EventBus()
    
    async def orchestrate_task(self, user_query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Main orchestration method that routes queries through appropriate agent chains"""
        session_id = self.generate_session_id()
        context = context or {}
        
        print(f"🎯 Starting orchestration for: '{user_query}'")
        
        # Parse intent and route to appropriate agent chain
        intent = self.parse_intent(user_query)
        result = await self.execute_agent_chain(intent, context, session_id)
        
        return {
            "session_id": session_id,
            "result": result,
            "agent_trace": self.get_agent_trace(session_id)
        }
    
    def parse_intent(self, query: str) -> Dict[str, Any]:
        """Parse user query to determine intent and routing"""
        lower_query = query.lower()
        
        if any(word in lower_query for word in ['best', 'find', 'buy', 'search']):
            return {"type": "CAR_SEARCH", "agent": "buyer", "query": query}
        elif any(word in lower_query for word in ['sell', 'value', 'price']):
            return {"type": "CAR_VALUATION", "agent": "seller", "query": query}
        elif any(word in lower_query for word in ['service', 'maintenance', 'repair']):
            return {"type": "MAINTENANCE", "agent": "owner", "query": query}
        elif any(word in lower_query for word in ['document', 'verify', 'papers']):
            return {"type": "DOCUMENT_VERIFICATION", "agent": "document", "query": query}
        
        return {"type": "GENERAL", "agent": "buyer", "query": query}
    
    async def execute_agent_chain(self, intent: Dict[str, Any], context: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """Execute the appropriate chain of agents based on intent"""
        agent_chain = self.build_agent_chain(intent)
        result = {"query": intent["query"], "context": context}
        
        for agent_config in agent_chain:
            agent = await self.get_agent(agent_config["name"])
            print(f"🤖 {agent_config['name'].title()} Agent processing...")
            
            result = await agent.process(result, agent_config.get("params", {}))
            self.log_agent_action(session_id, agent_config["name"], result)
        
        return result
    
    def build_agent_chain(self, intent: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Build the chain of agents to execute based on intent type"""
        intent_type = intent["type"]
        
        chains = {
            "CAR_SEARCH": [
                {"name": "buyer", "params": {"action": "search"}},
                {"name": "rag", "params": {"domain": "automotive"}},
                {"name": "valuation", "params": {"action": "price_check"}},
                {"name": "loan", "params": {"action": "pre_check"}},
                {"name": "dealer", "params": {"action": "book_test_drive"}}
            ],
            "CAR_VALUATION": [
                {"name": "document", "params": {"action": "verify"}},
                {"name": "valuation", "params": {"action": "full_assessment"}},
                {"name": "seller", "params": {"action": "create_listing"}}
            ],
            "MAINTENANCE": [
                {"name": "owner", "params": {"action": "maintenance_check"}},
                {"name": "dealer", "params": {"action": "book_service"}}
            ],
            "DOCUMENT_VERIFICATION": [
                {"name": "document", "params": {"action": "full_verification"}}
            ]
        }
        
        return chains.get(intent_type, [{"name": "buyer", "params": {"action": "general"}}])
    
    async def get_agent(self, agent_name: str):
        """Get or create agent instance"""
        if agent_name not in self.active_agents:
            try:
                # Dynamic import of agent class
                module_name = f"app.agents.{agent_name}_agent"
                agent_module = importlib.import_module(module_name)
                agent_class_name = f"{agent_name.title()}Agent"
                agent_class = getattr(agent_module, agent_class_name)
                self.active_agents[agent_name] = agent_class()
            except (ImportError, AttributeError) as e:
                print(f"Warning: Could not load {agent_name} agent: {e}")
                # Return a mock agent for demo purposes
                self.active_agents[agent_name] = MockAgent(agent_name)
        
        return self.active_agents[agent_name]
    
    def generate_session_id(self) -> str:
        """Generate unique session ID"""
        return f"session_{int(datetime.now().timestamp())}_{str(uuid.uuid4())[:8]}"
    
    def log_agent_action(self, session_id: str, agent_name: str, result: Dict[str, Any]):
        """Log agent actions for tracing"""
        if session_id not in self.agent_traces:
            self.agent_traces[session_id] = []
        
        self.agent_traces[session_id].append(AgentTrace(
            agent=f"{agent_name.title()} Agent",
            timestamp=datetime.now().isoformat(),
            action=result.get("action", "process"),
            output=result.get("summary", "Processing completed")
        ))
    
    def get_agent_trace(self, session_id: str) -> List[AgentTrace]:
        """Get agent execution trace for session"""
        return self.agent_traces.get(session_id, [])
    
    def get_agent_capabilities(self) -> List[Dict[str, Any]]:
        """Return list of all agent capabilities"""
        return [
            {
                "name": "Buyer Agent",
                "description": "Helps buyers find cars, compare options, and coordinate purchases",
                "capabilities": ["car_search", "financing_options", "test_drive_booking"]
            },
            {
                "name": "Seller Agent", 
                "description": "Assists sellers with valuation, listing creation, and fraud prevention",
                "capabilities": ["car_valuation", "listing_optimization", "fraud_detection"]
            },
            {
                "name": "Owner Agent",
                "description": "Manages vehicle ownership lifecycle including maintenance and insurance",
                "capabilities": ["maintenance_scheduling", "insurance_management", "predictive_maintenance"]
            },
            {
                "name": "Document Agent",
                "description": "Verifies documents, detects fraud, and integrates with government APIs",
                "capabilities": ["document_verification", "fraud_detection", "government_api_integration"]
            },
            {
                "name": "Dealer Agent",
                "description": "Manages dealer operations, inventory, and customer interactions",
                "capabilities": ["inventory_management", "test_drive_booking", "offer_negotiation"]
            },
            {
                "name": "RAG Agent",
                "description": "Provides market intelligence and expert knowledge retrieval",
                "capabilities": ["market_analysis", "expert_insights", "competitive_intelligence"]
            },
            {
                "name": "Loan Agent",
                "description": "Handles financing options, loan pre-approval, and subsidy information",
                "capabilities": ["loan_comparison", "pre_approval", "subsidy_calculation"]
            }
        ]

class EventBus:
    """Simple event bus for agent communication"""
    def __init__(self):
        self.listeners = {}
    
    def on(self, event: str, callback):
        if event not in self.listeners:
            self.listeners[event] = []
        self.listeners[event].append(callback)
    
    def emit(self, event: str, data: Any):
        if event in self.listeners:
            for callback in self.listeners[event]:
                callback(data)

class MockAgent:
    """Mock agent for demonstration when actual agent is not available"""
    def __init__(self, name: str):
        self.name = f"{name.title()} Agent"
    
    async def process(self, input_data: Dict[str, Any], params: Dict[str, Any] = None) -> Dict[str, Any]:
        return {
            **input_data,
            "action": f"{self.name.lower()}_processing",
            "summary": f"{self.name} completed processing",
            "mock": True
        }