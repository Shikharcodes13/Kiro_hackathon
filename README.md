# AutoAgent - LangChain-Powered Agentic Automotive Platform

## 🚗 Overview
An intelligent multi-agent ecosystem for the automotive industry where specialized AI agents powered by LangChain collaborate to handle car buying, selling, and ownership with zero human intervention.

## ⚡ Key Features
- **LangChain Integration** - Advanced AI agents with memory, tools, and reasoning
- **RAG (Retrieval-Augmented Generation)** - Comprehensive automotive knowledge base
- **Multi-Agent Orchestration** - Seamless collaboration between specialized agents
- **Real-time Processing** - FastAPI backend with async processing
- **Fallback Mode** - Works without API keys for development/demo

## 🤖 Agent Architecture

### Core LangChain Agents
- **🤝 Buyer Agent** - Car discovery with LangChain tools and memory
- **💸 Seller Agent** - Vehicle valuation with market intelligence
- **🛠️ Owner Agent** - Insurance and maintenance management
- **📑 Document Agent** - AI-powered document verification
- **📊 Dealer Agent** - Dashboard and booking management
- **🧠 RAG Agent** - Vector-based knowledge retrieval with FAISS
- **💰 Loan Agent** - Financing analysis and pre-approval

### LangChain Features Used
- **Agents & Tools** - Custom tools for each agent domain
- **Memory** - Conversation history and context retention
- **Prompts** - Specialized prompts for automotive domain
- **Vector Stores** - FAISS for knowledge base search
- **Embeddings** - OpenAI embeddings for semantic search

## 🎯 Hackathon Demo Flow (3 Minutes)
1. **User Query**: "Best EV under ₹15L in Delhi?"
2. **Buyer Agent** → Uses LangChain tools to extract criteria
3. **RAG Agent** → Vector search for market intelligence
4. **Valuation Agent** → AI-powered pricing analysis
5. **Loan Agent** → Financing options with subsidies
6. **Result** → Comprehensive recommendation with reasoning

## 🚀 Quick Start

### 1. Setup Backend
```bash
# Clone and setup
git clone <repo>
cd autoagent-platform

# Run setup script
python setup.py
```

### 2. Environment Configuration
```bash
# Edit .env file
OPENAI_API_KEY=your_api_key_here
LLM_MODEL=gpt-3.5-turbo
```

### 3. Start Full-Stack Application
```bash
# Start both backend and frontend
python start_fullstack.py

# Or start individually:
# Backend: python main.py
# Frontend: cd frontend && npm install && npm start
```

### 4. Access the Application
- **Frontend**: http://localhost:3000 (Porsche-inspired UI)
- **Backend API**: http://localhost:8000 (FastAPI docs)
- **Interactive Demo**: python demo_langchain.py

### 5. API Usage
```bash
# Test the API directly
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "Best EV under ₹15L in Delhi?"}'
```

## 📁 Project Structure
```
app/
├── agents/              # LangChain-powered agents
│   ├── buyer_agent.py   # Car search with tools & memory
│   ├── rag_agent.py     # Vector-based knowledge retrieval
│   ├── valuation_agent.py
│   └── loan_agent.py
├── orchestrator/        # Multi-agent coordination
│   └── task_manager.py  # Agent chain execution
├── models/              # Pydantic schemas
│   └── schemas.py
frontend/                # React frontend
├── src/
│   ├── components/      # React components
│   │   ├── HeroSection.js      # Porsche-inspired landing
│   │   ├── ChatInterface.js    # Conversational UI
│   │   ├── CarCard.js          # Car display cards
│   │   ├── AgentStatus.js      # Real-time agent status
│   │   └── AgentThinking.js    # AI decision visualization
│   ├── App.js           # Main React app
│   └── index.css        # Tailwind styles
├── package.json         # Frontend dependencies
└── tailwind.config.js   # Design system config
main.py                  # FastAPI server
demo_langchain.py        # Interactive demo
start_fullstack.py       # Full-stack startup script
requirements.txt         # LangChain dependencies
```

## 🛠️ Technical Stack

### Backend
- **FastAPI** - Modern Python web framework
- **LangChain** - AI agent framework with tools & memory
- **OpenAI** - GPT models for natural language processing
- **FAISS** - Vector database for knowledge retrieval
- **Pydantic** - Data validation and serialization

### Frontend
- **React 18** - Modern React with hooks
- **Tailwind CSS** - Utility-first styling framework
- **Framer Motion** - Smooth animations and transitions
- **Axios** - HTTP client for API communication
- **Lucide React** - Beautiful icon library

### AI Features
- **Multi-Agent System** - Specialized agents for different tasks
- **RAG (Retrieval-Augmented Generation)** - Knowledge-enhanced responses
- **Vector Search** - Semantic search through automotive data
- **Conversation Memory** - Context-aware multi-turn conversations

## 🎮 Demo Modes

### 1. Automated Demo
Shows complete agent collaboration flow
```bash
python demo_langchain.py
# Choose option 1
```

### 2. Interactive Demo
Chat with the agents directly
```bash
python demo_langchain.py
# Choose option 2
```

### 3. API Demo
```bash
curl http://localhost:8000/demo
```

## 🔧 Configuration

### With OpenAI API Key
- Full LangChain features
- Vector search capabilities
- Advanced reasoning
- Memory retention

### Without API Key (Fallback Mode)
- Basic agent functionality
- Mock responses
- Demo capabilities
- Development testing

## 🏆 Hackathon Winning Features

### 1. **Agent Collaboration**
Watch multiple AI agents work together in real-time

### 2. **LangChain Integration**
Advanced AI capabilities with tools, memory, and reasoning

### 3. **RAG Knowledge Base**
Vector-based search through comprehensive automotive data

### 4. **Indian Market Focus**
Specialized for Indian automotive market with local insights

### 5. **Zero Human Intervention**
Complete automation from query to recommendation

## 📊 API Endpoints

- `GET /` - Platform overview
- `POST /query` - Main agent processing
- `GET /demo` - Hackathon demo flow
- `GET /agents` - List all agents
- `GET /health` - Health check

## 🔍 Example Queries

```python
# Car search
"Best EV under ₹15L in Delhi?"

# Comparison
"Compare Tata Nexon EV vs MG ZS EV"

# Financing
"What are the loan options for Hyundai Kona Electric?"

# Market insights
"EV market trends in India 2024"
```

## 🚀 Deployment

### Local Development
```bash
python main.py
# Server runs on http://localhost:8000
```

### Production
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 🤝 Contributing
1. Fork the repository
2. Create feature branch
3. Add LangChain enhancements
4. Test with demo script
5. Submit pull request

## 📝 License
MIT License - Build amazing automotive AI!