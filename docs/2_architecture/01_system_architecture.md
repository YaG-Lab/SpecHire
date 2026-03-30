# SpecHire System Architecture
## HR SKILL - JD Analysis & CV Semantic Scoring

**Version:** 1.0  
**Date:** 2026-03-26  
**Status:** Design Phase

---

## Table of Contents
1. [Architecture Overview](#1-architecture-overview)
2. [System Context](#2-system-context)
3. [High-Level Architecture](#3-high-level-architecture)
4. [Component Architecture](#4-component-architecture)
5. [Data Architecture](#5-data-architecture)
6. [Integration Architecture](#6-integration-architecture)
7. [Deployment Architecture](#7-deployment-architecture)
8. [Security Architecture](#8-security-architecture)

---

## 1. Architecture Overview

### 1.1 Architecture Principles

| Principle | Description | Impact |
|-----------|-------------|--------|
| **Modularity** | SKILL-based architecture with loosely coupled components | Easy to extend and maintain |
| **Scalability** | Horizontal scaling for compute-intensive operations | Handle growing user base |
| **Observability** | Comprehensive logging, metrics, and tracing | Fast troubleshooting |
| **Security First** | Defense in depth, encryption, RBAC | Protect sensitive HR data |
| **Human-in-the-Loop** | AI assists but humans decide | Maintain accountability |
| **Explainability** | All AI decisions are transparent | Build trust and compliance |

### 1.2 Key Quality Attributes

```mermaid
mindmap
  root((Quality Attributes))
    Performance
      JD Generation under 10s
      CV Batch under 5min
      API Response under 2s
    Reliability
      99.5% Uptime
      Zero Data Loss
      Graceful Degradation
    Security
      PII Encryption
      RBAC
      Audit Logging
    Usability
      Intuitive UI
      Real-time Feedback
      Mobile Responsive
    Maintainability
      Modular SKILLs
      Clean APIs
      Comprehensive Tests
```

---

## 2. System Context

### 2.1 Context Diagram

```mermaid
C4Context
    title System Context - SpecHire Platform

    Person(hr, "HR Recruiter", "Primary user managing recruitment")
    Person(sem, "SE Manager", "Technical hiring manager")
    Person(admin, "HR Admin", "Views analytics and reports")
    Person(sysadmin, "System Admin", "Manages system config")
    
    System(spechire, "SpecHire Platform", "AI-powered recruitment system")
    
    System_Ext(llm, "LLM Services", "OpenAI/Anthropic")
    System_Ext(job_boards, "Job Boards", "LinkedIn, TopCV, ITviec")
    System_Ext(salary_db, "Salary APIs", "Market compensation data")
    System_Ext(gcal, "Google Calendar", "Interview scheduling")
    System_Ext(email, "Email Service", "SendGrid/SES")
    System_Ext(sso, "SSO Provider", "Company authentication")
    
    Rel(hr, spechire, "Creates JDs, Analyzes CVs", "HTTPS")
    Rel(sem, spechire, "Reviews candidates, Provides feedback", "HTTPS")
    Rel(admin, spechire, "Views reports", "HTTPS")
    Rel(sysadmin, spechire, "Configures system", "HTTPS")
    
    Rel(spechire, llm, "Generates content, Analyzes CVs", "API")
    Rel(spechire, job_boards, "Posts jobs, Tracks status", "API")
    Rel(spechire, salary_db, "Fetches salary benchmarks", "API")
    Rel(spechire, gcal, "Syncs interview schedules", "API")
    Rel(spechire, email, "Sends notifications", "SMTP/API")
    Rel(spechire, sso, "Authenticates users", "OAuth2/SAML")
```

### 2.2 User Roles & Interactions

| Role | Primary Actions | Key Interactions |
|------|----------------|------------------|
| **HR Recruiter** | Upload JDs, Analyze CVs, Schedule interviews | JD SKILL, CV SKILL, Interview Manager |
| **SE Manager** | Submit requirements, Review candidates, Interview | JD Input, Candidate Review, Feedback |
| **HR Admin** | View analytics, Monitor campaigns | Reporting Dashboard, Analytics Engine |
| **System Admin** | Configure AI, Manage users, System settings | Admin Panel, SKILL Config |

---

## 3. High-Level Architecture

### 3.1 Layered Architecture

```mermaid
graph TB
    subgraph "Presentation Layer"
        A[Web UI - React/Vue]
        B[Mobile Responsive]
        C[Real-time WebSocket]
    end
    
    subgraph "API Layer"
        D[API Gateway]
        E[REST APIs]
        F[GraphQL Optional]
        G[WebSocket Server]
    end
    
    subgraph "Application Layer - HR Agent Orchestrator"
        H[Intent Classifier]
        I[Context Manager]
        J[Workflow Orchestrator]
        K[SKILL Router]
    end
    
    subgraph "SKILL Layer - Core Intelligence"
        L[JD Analysis SKILL]
        M[CV Analysis SKILL]
        N[Interview SKILL Future]
        O[Analytics SKILL Future]
    end
    
    subgraph "Integration Layer"
        P[LLM Gateway]
        Q[Job Board Adapters]
        R[External API Connectors]
        S[Email/SMS Service]
    end
    
    subgraph "Data Layer"
        T[(PostgreSQL + pgvector)]
        U[(Redis Cache)]
        V[S3 Object Storage]
        W[Vector DB Pinecone]
    end
    
    A --> D
    B --> D
    C --> G
    D --> E
    D --> F
    E --> H
    G --> H
    H --> I
    I --> J
    J --> K
    K --> L
    K --> M
    K --> N
    K --> O
    L --> P
    M --> P
    L --> R
    M --> R
    J --> S
    L --> T
    M --> T
    L --> U
    M --> U
    L --> V
    M --> V
    M --> W
    
    style L fill:#4CAF50
    style M fill:#4CAF50
    style H fill:#2196F3
    style J fill:#2196F3
```

### 3.2 Architecture Patterns

#### Pattern 1: SKILL-Based Architecture
```
┌─────────────────────────────────────────┐
│         HR Agent Orchestrator           │
│  (Coordinates workflows & context)      │
└────────────┬────────────────────────────┘
             │
    ┌────────┴────────┐
    │   SKILL Router   │
    │  (Discovers &    │
    │   invokes SKILLs)│
    └────────┬────────┘
             │
   ┌─────────┴─────────────┐
   │                       │
┌──▼──────────┐    ┌──────▼───────┐
│  JD SKILL   │    │  CV SKILL    │
│  ┌────────┐ │    │  ┌─────────┐ │
│  │Parser  │ │    │  │Parser   │ │
│  │Generator│ │    │  │Finger-  │ │
│  │Intel   │ │    │  │printer  │ │
│  └────────┘ │    │  │Matcher  │ │
│             │    │  └─────────┘ │
└─────────────┘    └──────────────┘
```

**Benefits:**
- Independent development & deployment
- Reusable across different contexts
- Easy to test in isolation
- Can be versioned independently

#### Pattern 2: Event-Driven Processing
```
User Action → Event Bus → SKILL Processing → Results
     │                         │
     └─── Real-time ───────────┘
         Progress Updates
```

#### Pattern 3: CQRS for Analytics
```
Write Model:                Read Model:
JD/CV Operations  ──→  Event Store  ──→  Analytics Views
                              │
                              └──→  Reporting DB
```

---

## 4. Component Architecture

### 4.1 JD Analysis SKILL - Detailed Architecture

```mermaid
graph TB
    subgraph "JD Analysis SKILL"
        subgraph "Input Processing"
            A[API Endpoint] --> B[Input Validator]
            B --> C[Document Parser]
            C --> D[Requirement Extractor]
        end
        
        subgraph "Generation Engine"
            D --> E[Template Selector]
            E --> F[LLM Generator]
            F --> G[Content Formatter]
        end
        
        subgraph "Bi-directional Intelligence"
            G --> H[Parallel Analysis]
            H --> I[Attract Score Predictor]
            H --> J[Gap Detector]
            H --> K[Bias Auditor]
            H --> L[Salary Benchmarker]
        end
        
        subgraph "Output Assembly"
            I --> M[Intelligence Aggregator]
            J --> M
            K --> M
            L --> M
            G --> M
            M --> N[Version Manager]
            N --> O[Response Builder]
        end
        
        subgraph "Data Persistence"
            O --> P[(JD Repository)]
            O --> Q[(Version History)]
            O --> R[Cache Layer]
        end
        
        subgraph "External Dependencies"
            F -.->|LLM API| S[OpenAI/Claude]
            L -.->|Salary Data| T[Salary APIs]
            I -.->|Market Data| U[Job Board Analytics]
        end
    end
    
    style I fill:#FFC107
    style J fill:#FFC107
    style K fill:#FFC107
    style L fill:#FFC107
    style F fill:#4CAF50
```

**Component Responsibilities:**

| Component | Responsibility | Technology |
|-----------|---------------|------------|
| **Document Parser** | Extract text from Word/PDF | python-docx, PyPDF2, pytesseract |
| **Requirement Extractor** | NLP to identify key requirements | spaCy, transformers |
| **LLM Generator** | Generate professional JD content | LangChain + GPT-4/Claude |
| **Attract Score Predictor** | ML model to predict application rate | Custom trained model |
| **Gap Detector** | Logic to find contradictions | Rule engine + LLM |
| **Bias Auditor** | Scan for discriminatory language | Pattern matching + LLM |
| **Salary Benchmarker** | Real-time salary comparison | External API integration |

### 4.2 CV Semantic Analysis SKILL - Detailed Architecture

```mermaid
graph TB
    subgraph "CV Analysis SKILL"
        subgraph "Batch Processing"
            A[Batch Upload API] --> B[File Validator]
            B --> C[Queue Manager]
            C --> D[Parallel Worker Pool]
        end
        
        subgraph "CV Processing Pipeline"
            D --> E[Document Parser]
            E --> F[Structure Extractor]
            F --> G[Entity Recognizer]
        end
        
        subgraph "Depth Fingerprinting Engine"
            G --> H[Fingerprint Orchestrator]
            H --> I[Complexity Analyzer]
            H --> J[Scale Analyzer]
            H --> K[Progression Analyzer]
            H --> L[Consistency Analyzer]
            
            I --> M[Technical Fingerprint]
            J --> M
            K --> M
            L --> M
        end
        
        subgraph "Matching & Scoring"
            M --> N[JD Requirements Loader]
            N --> O[Semantic Matcher]
            O --> P[Score Calculator]
            P --> Q[Auto-Categorizer]
        end
        
        subgraph "Explainability"
            Q --> R[Why Rejected Engine]
            R --> S[Blind Spot Detector]
            S --> T[Explanation Generator]
        end
        
        subgraph "Results & Learning"
            T --> U[Results Aggregator]
            U --> V[Batch Results DB]
            U --> W[Real-time Progress]
            
            X[HR Override Tracker] --> Y[Closed-loop Learner]
            Y --> H
        end
        
        subgraph "External Dependencies"
            E -.->|OCR| Z[Tesseract]
            O -.->|Embeddings| AA[Vector DB]
            I -.->|LLM Analysis| AB[OpenAI/Claude]
        end
    end
    
    style I fill:#9C27B0
    style J fill:#9C27B0
    style K fill:#9C27B0
    style L fill:#9C27B0
    style R fill:#FF5722
    style S fill:#FF5722
```

**Component Responsibilities:**

| Component | Responsibility | Technology |
|-----------|---------------|------------|
| **Queue Manager** | Async batch processing | RabbitMQ/Celery |
| **Document Parser** | Multi-format CV parsing | Textract, PyPDF2 |
| **Structure Extractor** | Identify CV sections | Custom NLP + patterns |
| **Complexity Analyzer** | Evaluate technical depth | LLM + heuristics |
| **Scale Analyzer** | Extract quantitative metrics | Regex + NER |
| **Progression Analyzer** | Career trajectory analysis | Timeline analysis |
| **Consistency Analyzer** | Domain focus & stability | Graph analysis |
| **Semantic Matcher** | Deep CV-JD matching | Embeddings + cosine similarity |
| **Why Rejected Engine** | Explainable rejection reasons | Taxonomy classifier |
| **Blind Spot Detector** | Find false negatives | ML model + rules |

### 4.3 HR Agent Orchestrator Architecture

```mermaid
graph LR
    subgraph "HR Agent Orchestrator"
        A[User Input] --> B[Intent Classifier]
        B --> C{Intent Type}
        
        C -->|Create JD| D[JD Workflow Manager]
        C -->|Analyze CVs| E[CV Workflow Manager]
        C -->|Schedule Interview| F[Interview Workflow Manager]
        C -->|View Analytics| G[Analytics Workflow Manager]
        
        D --> H[Context Manager]
        E --> H
        F --> H
        G --> H
        
        H --> I[SKILL Router]
        I --> J[JD SKILL]
        I --> K[CV SKILL]
        I --> L[Other SKILLs]
        
        J --> M[Response Formatter]
        K --> M
        L --> M
        
        M --> N[User Output]
    end
    
    style B fill:#2196F3
    style H fill:#FF9800
    style I fill:#4CAF50
```

**Orchestrator Responsibilities:**
1. **Intent Classification** - Understand user goals from natural language
2. **Context Management** - Maintain conversation state, user preferences, campaign context
3. **SKILL Routing** - Select and invoke appropriate SKILLs
4. **Workflow Coordination** - Manage multi-step processes
5. **Response Formatting** - Present results in user-friendly format

---

## 5. Data Architecture

### 5.1 Database Schema - Core Entities

```mermaid
erDiagram
    USERS ||--o{ CAMPAIGNS : creates
    CAMPAIGNS ||--o{ JOB_DESCRIPTIONS : contains
    JOB_DESCRIPTIONS ||--o{ JD_VERSIONS : has
    JOB_DESCRIPTIONS ||--o{ JD_MARKET_ANALYSIS : analyzed_by
    CAMPAIGNS ||--o{ CANDIDATES : receives
    CANDIDATES ||--o{ CV_ANALYSIS_RESULTS : has
    CANDIDATES ||--o{ INTERVIEWS : scheduled_for
    JOB_DESCRIPTIONS ||--o{ CV_ANALYSIS_RESULTS : evaluated_against
    
    USERS {
        id uuid PK
        email string
        role string
        created_at timestamp
    }
    
    CAMPAIGNS {
        id uuid PK
        created_by uuid FK
        name string
        status string
        start_date timestamp
        end_date timestamp
    }
    
    JOB_DESCRIPTIONS {
        id uuid PK
        campaign_id uuid FK
        job_title string
        job_description text
        mandatory_requirements jsonb
        preferred_requirements jsonb
        benefits jsonb
        status string
        version_number int
        created_at timestamp
    }
    
    JD_VERSIONS {
        id uuid PK
        jd_id uuid FK
        version_number int
        content jsonb
        edited_by uuid FK
        created_at timestamp
    }
    
    JD_MARKET_ANALYSIS {
        id uuid PK
        jd_id uuid FK
        attract_score float
        attract_factors jsonb
        requirement_gaps jsonb
        bias_alerts jsonb
        salary_benchmark jsonb
        analyzed_at timestamp
    }
    
    CANDIDATES {
        id uuid PK
        campaign_id uuid FK
        name string
        email string
        phone string
        cv_file_path string
        uploaded_at timestamp
    }
    
    CV_ANALYSIS_RESULTS {
        id uuid PK
        candidate_id uuid FK
        jd_id uuid FK
        parsed_cv jsonb
        technical_fingerprint jsonb
        matching_score float
        score_breakdown jsonb
        category string
        explainability jsonb
        blind_spot_alert boolean
        analyzed_at timestamp
    }
    
    INTERVIEWS {
        id uuid PK
        candidate_id uuid FK
        interviewer_id uuid FK
        scheduled_at timestamp
        status string
        meeting_link string
        feedback jsonb
    }
```

### 5.2 Data Flow Architecture

```mermaid
flowchart TB
    subgraph "Data Sources"
        A[User Input]
        B[Document Upload]
        C[External APIs]
    end
    
    subgraph "Data Ingestion Layer"
        D[API Gateway]
        E[File Storage Service]
        F[API Connectors]
    end
    
    subgraph "Processing Layer"
        G[Stream Processor]
        H[Batch Processor]
        I[Real-time Processor]
    end
    
    subgraph "Storage Layer"
        J[(Primary DB<br/>PostgreSQL)]
        K[(Cache<br/>Redis)]
        L[Object Storage<br/>S3]
        M[(Vector DB<br/>Pinecone)]
        N[(Analytics DB<br/>ClickHouse)]
    end
    
    subgraph "Serving Layer"
        O[Query Service]
        P[Analytics Service]
        Q[Search Service]
    end
    
    A --> D
    B --> E
    C --> F
    
    D --> G
    E --> H
    F --> I
    
    G --> J
    G --> K
    H --> J
    H --> L
    I --> M
    I --> N
    
    J --> O
    K --> O
    L --> O
    M --> Q
    N --> P
    
    style J fill:#4CAF50
    style K fill:#FF9800
    style L fill:#2196F3
    style M fill:#9C27B0
```

### 5.3 Data Partitioning Strategy

**Campaign-based Partitioning:**
```sql
-- Partition JD and CV data by campaign
CREATE TABLE cv_analysis_results (
    id UUID PRIMARY KEY,
    campaign_id UUID NOT NULL,
    candidate_id UUID NOT NULL,
    -- ... other fields
) PARTITION BY HASH (campaign_id);

-- Archive old campaigns
-- Campaigns > 12 months → Archive DB (read-only)
```

**Benefits:**
- Better query performance (scan only relevant partitions)
- Easy archival (drop old partitions)
- Parallel processing (process partitions independently)

---

## 6. Integration Architecture

### 6.1 Integration Patterns

```mermaid
graph TB
    subgraph "SpecHire Platform"
        A[HR Agent Core]
    end
    
    subgraph "External Services"
        B[LLM Services<br/>OpenAI/Anthropic]
        C[Job Boards<br/>LinkedIn/TopCV]
        D[Salary APIs<br/>Glassdoor/Payscale]
        E[Google Calendar]
        F[Email Service<br/>SendGrid]
        G[SSO Provider]
    end
    
    A -->|Direct API| B
    A -->|Adapter Pattern| C
    A -->|API Gateway| D
    A -->|OAuth2 + Sync| E
    A -->|Queue + Batch| F
    A -->|SAML/OAuth2| G
    
    style B fill:#FFC107
    style C fill:#4CAF50
    style D fill:#2196F3
```

### 6.2 Integration Components

#### LLM Gateway (Unified LLM Access)
```
┌─────────────────────────────────────┐
│         LLM Gateway                 │
│  ┌────────────────────────────┐    │
│  │  Provider Abstraction      │    │
│  │  - OpenAI (GPT-4)         │    │
│  │  - Anthropic (Claude)     │    │
│  │  - Azure OpenAI           │    │
│  └────────────────────────────┘    │
│  ┌────────────────────────────┐    │
│  │  Features:                 │    │
│  │  - Retry & Circuit Breaker│    │
│  │  - Rate Limiting          │    │
│  │  - Cost Tracking          │    │
│  │  - Fallback Strategy      │    │
│  └────────────────────────────┘    │
└─────────────────────────────────────┘
```

#### Job Board Adapter (Plugin Architecture)
```
┌─────────────────────────────────────┐
│     Job Board Adapter Manager       │
│  ┌────────┐  ┌────────┐  ┌───────┐ │
│  │LinkedIn│  │ TopCV  │  │ITviec │ │
│  │Adapter │  │Adapter │  │Adapter│ │
│  └────────┘  └────────┘  └───────┘ │
│                                     │
│  Common Interface:                  │
│  - post_job()                      │
│  - get_status()                    │
│  - unpublish_job()                 │
│  - get_analytics()                 │
└─────────────────────────────────────┘
```

### 6.3 API Integration Matrix

| Service | Protocol | Auth | Rate Limit | SLA | Fallback |
|---------|----------|------|------------|-----|----------|
| OpenAI GPT-4 | REST | API Key | 10K TPM | 99.9% | Claude |
| Anthropic Claude | REST | API Key | Custom | 99.9% | GPT-4 |
| LinkedIn | OAuth2 | OAuth2 | 100/day | 99% | Manual post |
| Google Calendar | REST | OAuth2 | 10K/day | 99.9% | Local cache |
| SendGrid | REST | API Key | 100/sec | 99.95% | AWS SES |
| Salary APIs | REST | API Key | 1K/day | 95% | Cached data |

---

## 7. Deployment Architecture

### 7.1 Kubernetes Deployment Architecture

```mermaid
graph TB
    subgraph "External Load Balancer"
        A[AWS ALB / GCP LB]
    end
    
    subgraph "Kubernetes Cluster"
        subgraph "Ingress Layer"
            B[NGINX Ingress]
        end
        
        subgraph "Application Pods"
            C[API Gateway<br/>3 replicas]
            D[HR Agent Orchestrator<br/>3 replicas]
            E[JD SKILL Service<br/>3 replicas]
            F[CV SKILL Service<br/>5 replicas]
            G[Worker Pool<br/>10 replicas]
        end
        
        subgraph "Supporting Services"
            H[Redis<br/>Primary + Replica]
            I[RabbitMQ<br/>Cluster]
        end
    end
    
    subgraph "Managed Services"
        J[(RDS PostgreSQL<br/>Multi-AZ)]
        K[S3 Object Storage]
        L[Pinecone Vector DB]
    end
    
    A --> B
    B --> C
    C --> D
    D --> E
    D --> F
    F --> G
    E --> H
    F --> H
    G --> I
    E --> J
    F --> J
    E --> K
    F --> K
    F --> L
    
    style C fill:#2196F3
    style D fill:#2196F3
    style E fill:#4CAF50
    style F fill:#4CAF50
    style G fill:#FF9800
```

### 7.2 Environment Architecture

```mermaid
graph LR
    subgraph "Development"
        A[Dev Cluster]
        B[Dev DB]
        C[Mock LLM]
    end
    
    subgraph "Staging"
        D[Staging Cluster]
        E[Staging DB]
        F[Real LLM<br/>Limited]
    end
    
    subgraph "Production"
        G[Prod Cluster<br/>Multi-Region]
        H[Prod DB<br/>Multi-AZ]
        I[Real LLM<br/>Full Quota]
    end
    
    A -->|CI/CD| D
    D -->|Approval| G
    
    style G fill:#4CAF50
    style H fill:#4CAF50
    style I fill:#4CAF50
```

### 7.3 Scaling Strategy

#### Horizontal Pod Autoscaler (HPA)
```yaml
# CV SKILL Service (CPU + Queue-based)
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: cv-skill-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: cv-skill-service
  minReplicas: 3
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: External
    external:
      metric:
        name: rabbitmq_queue_messages
      target:
        type: AverageValue
        averageValue: "30"
```

#### Vertical Pod Autoscaler (VPA)
```yaml
# JD SKILL Service (Memory optimization)
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: jd-skill-vpa
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: jd-skill-service
  updatePolicy:
    updateMode: "Auto"
```

---

## 8. Security Architecture

### 8.1 Security Layers

```mermaid
graph TB
    subgraph "Edge Security"
        A[WAF<br/>CloudFlare/AWS WAF]
        B[DDoS Protection]
        C[Rate Limiting]
    end
    
    subgraph "Network Security"
        D[VPC/Private Network]
        E[Network ACLs]
        F[Security Groups]
    end
    
    subgraph "Application Security"
        G[Authentication<br/>OAuth2/JWT]
        H[Authorization<br/>RBAC]
        I[API Gateway<br/>Auth]
    end
    
    subgraph "Data Security"
        J[Encryption at Rest<br/>AES-256]
        K[Encryption in Transit<br/>TLS 1.3]
        L[PII Masking]
    end
    
    subgraph "Secrets Management"
        M[HashiCorp Vault /<br/>AWS Secrets Manager]
    end
    
    A --> D
    B --> D
    C --> D
    D --> G
    E --> G
    F --> G
    G --> J
    H --> J
    I --> J
    J --> M
    K --> M
    L --> M
    
    style A fill:#F44336
    style G fill:#FF9800
    style J fill:#4CAF50
    style M fill:#2196F3
```

### 8.2 Authentication & Authorization Flow

```mermaid
sequenceDiagram
    actor User
    participant Client
    participant API Gateway
    participant Auth Service
    participant SSO
    participant Resource Service
    
    User->>Client: Login Request
    Client->>API Gateway: POST /auth/login
    API Gateway->>Auth Service: Validate & Route
    Auth Service->>SSO: OAuth2/SAML Request
    SSO-->>Auth Service: User Profile + Token
    Auth Service->>Auth Service: Generate JWT<br/>(with roles)
    Auth Service-->>Client: JWT Token + Refresh Token
    
    Note over Client,Resource Service: Accessing Protected Resource
    
    Client->>API Gateway: GET /api/jd/analyze<br/>Authorization: Bearer {JWT}
    API Gateway->>API Gateway: Validate JWT Signature
    API Gateway->>API Gateway: Check RBAC Rules
    
    alt Authorized
        API Gateway->>Resource Service: Forward Request<br/>(with user context)
        Resource Service-->>API Gateway: Response
        API Gateway-->>Client: 200 OK + Data
    else Unauthorized
        API Gateway-->>Client: 403 Forbidden
    end
```

### 8.3 RBAC Model

```mermaid
graph TB
    subgraph "Roles"
        A[HR Recruiter]
        B[SE Manager]
        C[HR Admin]
        D[System Admin]
    end
    
    subgraph "Permissions"
        E[Create JD]
        F[Analyze CV]
        G[Schedule Interview]
        H[View Analytics]
        I[Manage Users]
        J[Configure System]
        K[View All Data]
        L[Export Data]
    end
    
    A --> E
    A --> F
    A --> G
    
    B --> H
    B -.->|Limited| F
    
    C --> H
    C --> K
    C --> L
    
    D --> I
    D --> J
    D --> K
    
    style A fill:#4CAF50
    style B fill:#2196F3
    style C fill:#FF9800
    style D fill:#F44336
```

### 8.4 Data Encryption Strategy

| Data Type | At Rest | In Transit | Key Management | Retention |
|-----------|---------|------------|---------------|-----------|
| **CV Files** | AES-256 (S3 SSE-KMS) | TLS 1.3 | AWS KMS | 12 months |
| **PII (Name, Email, Phone)** | Database-level encryption | TLS 1.3 | Vault | 12 months |
| **JD Content** | Standard DB encryption | TLS 1.3 | RDS encryption | Indefinite |
| **API Keys/Secrets** | Vault encryption | TLS 1.3 | Vault | Rotated 90 days |
| **Session Tokens** | Redis encryption | TLS 1.3 | App-level | 8 hours |
| **Audit Logs** | S3 Glacier encryption | TLS 1.3 | AWS KMS | 7 years |

### 8.5 Security Monitoring

```mermaid
graph LR
    subgraph "Security Events"
        A[Authentication Failures]
        B[Authorization Violations]
        C[Suspicious API Calls]
        D[Data Access Anomalies]
    end
    
    subgraph "SIEM System"
        E[Log Aggregation]
        F[Correlation Engine]
        G[Threat Detection]
    end
    
    subgraph "Response"
        H[Alert SOC]
        I[Auto-Block IP]
        J[Incident Ticket]
    end
    
    A --> E
    B --> E
    C --> E
    D --> E
    E --> F
    F --> G
    G --> H
    G --> I
    G --> J
    
    style G fill:#F44336
    style I fill:#FF9800
```

---

## 9. Architecture Decision Records (ADRs)

### ADR-001: SKILL-Based Architecture
**Status:** Accepted  
**Context:** Need modular, reusable AI capabilities  
**Decision:** Implement SKILL-based architecture with HR Agent orchestrator  
**Consequences:** 
- ✅ Independent development and scaling
- ✅ Easy to test and maintain
- ❌ Additional orchestration complexity

### ADR-002: Postgres + pgvector for Storage
**Status:** Accepted  
**Context:** Need relational data + vector similarity search  
**Decision:** Use PostgreSQL with pgvector extension  
**Consequences:**
- ✅ Single database for structured + vector data
- ✅ ACID transactions
- ❌ May need specialized vector DB at scale

### ADR-003: Async Batch Processing for CVs
**Status:** Accepted  
**Context:** CV analysis can take 30-60s per CV  
**Decision:** Use RabbitMQ + Worker pool for async processing  
**Consequences:**
- ✅ Non-blocking UI
- ✅ Horizontal scaling
- ❌ Need progress tracking mechanism

### ADR-004: LLM Gateway Abstraction
**Status:** Accepted  
**Context:** Multiple LLM providers (OpenAI, Anthropic)  
**Decision:** Create unified LLM Gateway with provider abstraction  
**Consequences:**
- ✅ Easy to switch providers
- ✅ Cost optimization via routing
- ❌ Additional abstraction layer

### ADR-005: Kubernetes for Deployment
**Status:** Accepted  
**Context:** Need auto-scaling, resilience, multi-environment  
**Decision:** Deploy on Kubernetes (AWS EKS / GCP GKE)  
**Consequences:**
- ✅ Auto-scaling and self-healing
- ✅ Easy multi-region deployment
- ❌ Operational complexity

---

## 10. Next Steps

### Phase 1: Foundation (Weeks 1-4)
- [ ] Setup development environment
- [ ] Implement basic API Gateway
- [ ] Create PostgreSQL schema
- [ ] Setup CI/CD pipeline

### Phase 2: Core SKILLs (Weeks 5-10)
- [ ] Implement JD Analysis SKILL
- [ ] Implement CV Semantic Analysis SKILL
- [ ] Setup LLM Gateway
- [ ] Integrate async processing

### Phase 3: Orchestration (Weeks 11-14)
- [ ] Build HR Agent Orchestrator
- [ ] Implement SKILL Router
- [ ] Create Context Manager
- [ ] Build Web UI

### Phase 4: Integration & Testing (Weeks 15-18)
- [ ] Integrate external services
- [ ] Performance testing
- [ ] Security audit
- [ ] User acceptance testing

### Phase 5: Deployment (Weeks 19-20)
- [ ] Production environment setup
- [ ] Data migration
- [ ] Training & documentation
- [ ] Go-live

---

**Document Control:**
- **Owner:** Architecture Team
- **Review Cycle:** Quarterly
- **Last Updated:** 2026-03-26
- **Next Review:** 2026-06-26
