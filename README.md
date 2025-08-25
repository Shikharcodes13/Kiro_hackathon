# Kira - AI-Powered Automotive Platform

A comprehensive automotive platform that combines Next.js frontend, NestJS API gateway, and multiple FastAPI ML services for OCR, RAG, valuation, and AI agent capabilities.

## Architecture

```
/KIRA
│── /frontend              # Next.js app (dealer/customer dashboard, WebRTC UI)
│── /gateway               # NestJS API gateway (auth, orchestration, DB)
│── /ml-services           # FastAPI apps for OCR, RAG, valuation, agent
│    ├── /ocr_service
│    ├── /rag_service
│    ├── /valuation_service
│    └── /agent_service
│── /shared                # Shared contracts/interfaces
│    ├── /schemas          # Pydantic / Zod schemas for API contracts
│    └── /utils            # Shared constants, logging utils
│── /infra                 # Deployment, Docker, k8s manifests, Terraform
│── /docs                  # Architecture diagrams, API contracts, workflows
```

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 18+
- Python 3.9+

### Development Setup

1. **Clone and setup**
   ```bash
   git clone <repository-url>
   cd Kira
   npm install
   ```

2. **Start all services**
   ```bash
   npm run dev
   ```

3. **Access services**
   - Frontend: http://localhost:3000
   - API Gateway: http://localhost:3001
   - OCR Service: http://localhost:8001
   - RAG Service: http://localhost:8002
   - Valuation Service: http://localhost:8003
   - Agent Service: http://localhost:8004

## Services Overview

### Frontend (Next.js)
- Dealer and customer dashboards
- WebRTC video calling interface
- Real-time notifications
- Document upload and management

### Gateway (NestJS)
- Authentication and authorization
- API orchestration
- Database management
- Service discovery and routing

### ML Services (FastAPI)

#### OCR Service
- Document text extraction
- Image preprocessing
- Multi-format support (PDF, images)

#### RAG Service
- Retrieval-Augmented Generation
- Document indexing and search
- Knowledge base management

#### Valuation Service
- Vehicle valuation algorithms
- Market data analysis
- Price prediction models

#### Agent Service
- AI agent orchestration
- Conversation management
- Task automation

## Development

### Available Scripts
- `npm run dev` - Start all services
- `npm run build` - Build all containers
- `npm run down` - Stop all services
- `npm run lint` - Lint all code
- `npm run test` - Run all tests

### Adding New Features
1. Create feature branch
2. Implement in appropriate service
3. Update shared schemas if needed
4. Add tests
5. Update documentation

## Deployment

See `/infra` directory for deployment configurations:
- Docker production builds
- Kubernetes manifests
- Terraform infrastructure (if applicable)

## Documentation

See `/docs` directory for:
- Architecture diagrams
- API contracts
- Workflow documentation
- Service integration guides

## Contributing

1. Follow the established directory structure
2. Use shared schemas for API contracts
3. Add comprehensive tests
4. Update documentation
5. Follow linting rules

## License

[Add your license here]
