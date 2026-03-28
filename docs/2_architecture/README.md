# SpecHire Architecture Documentation
## Complete Architecture Guide

---

## 📚 Document Index

This directory contains the complete architecture design for the SpecHire platform, focusing on the HR SKILL system for JD Analysis and CV Semantic Scoring.

### Documents Overview

| Document | Purpose | Audience |
|----------|---------|----------|
| **01_system_architecture.md** | Complete system architecture including layers, components, data flow, security, and deployment | Architects, Tech Leads, DevOps |
| **02_architecture_diagrams.md** | Visual Mermaid diagrams for all architectural views | All stakeholders |
| **03_skill_architecture_pattern.md** | SKILL design pattern, implementation guide, and best practices | Developers, Architects |

---

## 🎯 Quick Navigation

### For Different Roles

#### **Product Managers / Business Stakeholders**
Start with:
1. Section 2 in `01_system_architecture.md` - System Context
2. `02_architecture_diagrams.md` - Diagram #1 (System Context)
3. `02_architecture_diagrams.md` - Diagrams #5 & #6 (Data Flows)

**What you'll learn:** How users interact with the system, what problems it solves, and how workflows operate.

---

#### **Software Architects**
Start with:
1. `01_system_architecture.md` - Complete document (all sections)
2. `02_architecture_diagrams.md` - Diagrams #2, #3, #4 (Container & Component views)
3. `03_skill_architecture_pattern.md` - SKILL pattern deep dive
4. Section 9 in `01_system_architecture.md` - ADRs

**What you'll learn:** Architectural patterns, technology choices, trade-offs, and design decisions.

---

#### **Backend Developers**
Start with:
1. `03_skill_architecture_pattern.md` - Complete implementation guide
2. `02_architecture_diagrams.md` - Diagrams #3 & #4 (Component architecture)
3. Section 4 in `01_system_architecture.md` - Component details
4. Section 5 in `01_system_architecture.md` - Data architecture

**What you'll learn:** How to implement SKILLs, APIs, data models, and integration patterns.

---

#### **Frontend Developers**
Start with:
1. Section 3.1 in `01_system_architecture.md` - Layered architecture
2. `02_architecture_diagrams.md` - Diagrams #5 & #6 (Data flows)
3. Section 6 in `01_system_architecture.md` - API integration

**What you'll learn:** API contracts, data flows, WebSocket integration for real-time updates.

---

#### **DevOps / SRE**
Start with:
1. Section 7 in `01_system_architecture.md` - Deployment architecture
2. `02_architecture_diagrams.md` - Diagram #7 (Kubernetes)
3. Section 8 in `01_system_architecture.md` - Security architecture
4. `02_architecture_diagrams.md` - Diagrams #8, #9, #10 (Security, Monitoring, CI/CD)

**What you'll learn:** Infrastructure setup, scaling strategy, monitoring, and security controls.

---

#### **Security Engineers**
Start with:
1. Section 8 in `01_system_architecture.md` - Complete security architecture
2. `02_architecture_diagrams.md` - Diagram #8 (Security layers)
3. Section 6.3 in `01_system_architecture.md` - API integration security
4. Section 5.3 in `01_system_architecture.md` - Data encryption strategy

**What you'll learn:** Security controls, encryption, RBAC, compliance, and threat mitigation.

---

## 🏗️ Architecture Overview

### System Summary

**SpecHire** is an AI-powered recruitment platform built on a **SKILL-based architecture** that provides two core capabilities:

1. **JD Analysis & Generation SKILL**
   - Automated job description creation
   - Bi-directional market intelligence
   - Bias detection and salary benchmarking

2. **CV Semantic Analysis & Scoring SKILL**
   - Depth fingerprinting (beyond keywords)
   - Explainable AI categorization
   - Blind spot detection for false negatives

### Key Architectural Decisions

| Decision | Rationale |
|----------|-----------|
| **SKILL-based Architecture** | Modular, reusable AI capabilities that can be independently developed and scaled |
| **PostgreSQL + pgvector** | Single database for relational + vector data, ACID transactions |
| **Async Batch Processing** | Non-blocking UI, horizontal scaling for CV analysis |
| **LLM Gateway Abstraction** | Provider flexibility, cost optimization, fallback strategy |
| **Kubernetes Deployment** | Auto-scaling, resilience, multi-environment support |

---

## 📊 Architecture Diagrams at a Glance

### 1. System Context
Shows users, external systems, and high-level interactions.
```
[Users] → [SpecHire Platform] → [LLM Services, Job Boards, External APIs]
```

### 2. Container Architecture
Shows internal services and data stores.
```
Web UI → API Gateway → HR Agent → [JD SKILL, CV SKILL] → [Database, Cache, Queue]
```

### 3. Component Architecture - JD SKILL
Shows internal components of JD Analysis SKILL.
```
Input → Parser → Generator → [Intelligence Modules] → Output
```

### 4. Component Architecture - CV SKILL
Shows internal components of CV Analysis SKILL.
```
Batch → Worker Pool → [Fingerprinting] → Matcher → Explainer → Output
```

### 5. Data Flows
Shows step-by-step workflows for JD creation and CV analysis.

### 6. Deployment
Shows Kubernetes infrastructure with pods, services, and managed resources.

### 7. Security
Shows multiple security layers from edge to data.

### 8. Monitoring
Shows observability stack (metrics, logs, traces, alerts).

---

## 🔑 Key Concepts

### What is a SKILL?

A **SKILL** is a modular AI capability that:
- Encapsulates specific domain expertise
- Provides standard interface (input/output contracts)
- Can be composed with other SKILLs
- Learns from feedback (HITL - Human In The Loop)
- Is independently deployable and scalable

**Example:**
```
JD Analysis SKILL
├── Input: Requirement document
├── Processing: Parse → Extract → Generate → Analyze
└── Output: Professional JD + Market intelligence
```

### SKILL vs Microservice

| Aspect | Microservice | SKILL |
|--------|-------------|-------|
| Purpose | Business logic | AI intelligence |
| Interface | REST API | Intent-based |
| Learning | Static | Continuous |
| Composition | API calls | Semantic routing |

---

## 🔬 Technical Stack

### Backend
- **Language**: Python 3.11+
- **Framework**: FastAPI
- **LLM Integration**: LangChain, OpenAI, Anthropic
- **Document Processing**: PyPDF2, python-docx, pytesseract

### Data Layer
- **Primary DB**: PostgreSQL 15+ with pgvector
- **Cache**: Redis 7+
- **Object Storage**: S3-compatible
- **Vector DB**: Pinecone (or Qdrant)
- **Message Queue**: RabbitMQ

### Infrastructure
- **Container**: Docker
- **Orchestration**: Kubernetes (EKS/GKE)
- **Monitoring**: Prometheus + Grafana
- **Logging**: ELK Stack
- **Tracing**: Jaeger + OpenTelemetry

### External Services
- **LLM**: OpenAI GPT-4, Anthropic Claude
- **Job Boards**: LinkedIn, TopCV, ITviec APIs
- **Calendar**: Google Calendar API
- **Email**: SendGrid / AWS SES

---

## 📈 Performance Targets

### JD Analysis SKILL
- **Latency**: < 10s (P95) for JD generation
- **Throughput**: 10+ concurrent users
- **Availability**: 99.9%

### CV Analysis SKILL
- **Batch Processing**: 50 CVs in < 5 minutes
- **Per-CV Latency**: < 60s
- **Throughput**: 5+ concurrent batches
- **Availability**: 99.5%

---

## 🔒 Security Highlights

### Layers
1. **Edge**: WAF, DDoS protection, rate limiting
2. **Network**: VPC, security groups, network ACLs
3. **Application**: JWT auth, RBAC
4. **Data**: AES-256 encryption at rest, TLS 1.3 in transit
5. **Secrets**: HashiCorp Vault / AWS Secrets Manager

### Compliance
- **GDPR**: Data privacy, right to be forgotten
- **EEOC**: Bias auditing in AI decisions
- **SOC 2**: Security controls for HR data

---

## 🚀 Deployment Strategy

### Environments
- **Development**: Mock services, rapid iteration
- **Staging**: Full integration, pre-production testing
- **Production**: Multi-region, high availability

### Scaling
- **Horizontal Pod Autoscaler (HPA)**: CPU-based scaling
- **Vertical Pod Autoscaler (VPA)**: Memory optimization
- **Queue-based scaling**: RabbitMQ queue depth triggers

---

## 📝 Development Phases

### Phase 1: Foundation (Weeks 1-4)
- Development environment setup
- Basic API Gateway
- Database schema
- CI/CD pipeline

### Phase 2: Core SKILLs (Weeks 5-10)
- JD Analysis SKILL implementation
- CV Semantic Analysis SKILL implementation
- LLM Gateway
- Async processing

### Phase 3: Orchestration (Weeks 11-14)
- HR Agent Orchestrator
- SKILL Router
- Context Manager
- Web UI

### Phase 4: Integration (Weeks 15-18)
- External service integration
- Performance testing
- Security audit
- UAT

### Phase 5: Deployment (Weeks 19-20)
- Production setup
- Data migration
- Training & documentation
- Go-live

---

## 🔗 Related Resources

### Internal Documents
- `/docs/1_BA/3-specific_requirement.md` - Detailed requirements
- `/docs/1_BA/2-business_process.md` - Business workflows

### External References
- [C4 Model](https://c4model.com/) - Architecture documentation standard
- [Mermaid Diagrams](https://mermaid.js.org/) - Diagram syntax
- [FastAPI](https://fastapi.tiangolo.com/) - Backend framework
- [LangChain](https://python.langchain.com/) - LLM orchestration

---

## 💡 How to Use These Documents

### For Implementation
1. Read `03_skill_architecture_pattern.md` for implementation guide
2. Use diagrams from `02_architecture_diagrams.md` as reference
3. Follow coding examples in `03_skill_architecture_pattern.md`
4. Review ADRs in `01_system_architecture.md` for context

### For Review
1. Start with system context in `01_system_architecture.md`
2. Review relevant diagrams in `02_architecture_diagrams.md`
3. Deep dive into specific sections as needed
4. Check ADRs for architectural decisions

### For Onboarding
1. Read this README first
2. Review diagrams in `02_architecture_diagrams.md`
3. Read SKILL pattern in `03_skill_architecture_pattern.md`
4. Explore component details in `01_system_architecture.md`

---

## 🤝 Contributing to Architecture

### Process
1. Propose architectural change via ADR (Architecture Decision Record)
2. Discuss with architecture team
3. Update relevant documentation
4. Update diagrams if needed
5. Get approval before implementation

### ADR Template
```markdown
# ADR-XXX: [Title]

**Status:** Proposed | Accepted | Deprecated
**Context:** What is the problem?
**Decision:** What are we doing?
**Consequences:** What are the impacts?
**Alternatives Considered:** What else did we think about?
```

---

## 📞 Questions & Support

### Architecture Review
- **Team:** Architecture Team
- **Meeting:** Every Thursday 2pm
- **Slack:** #architecture-review

### Technical Support
- **Team:** Platform Team
- **Slack:** #platform-support
- **Email:** platform-team@example.com

---

## 📅 Document Maintenance

- **Review Cycle:** Quarterly
- **Owner:** Architecture Team
- **Last Updated:** 2026-03-26
- **Next Review:** 2026-06-26

---

## ✅ Checklist for New Developers

Before starting implementation, ensure you understand:

- [ ] System context and user roles
- [ ] SKILL architecture pattern
- [ ] JD Analysis SKILL workflow
- [ ] CV Analysis SKILL workflow
- [ ] Data models and schemas
- [ ] API contracts and integration patterns
- [ ] Security requirements
- [ ] Deployment architecture
- [ ] Monitoring and observability
- [ ] Testing strategy

---

**Note:** This architecture is designed to be evolutionary. As the system grows and requirements change, these documents will be updated to reflect the current state and future direction.
