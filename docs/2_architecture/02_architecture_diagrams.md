# SpecHire Architecture Diagrams
## Visual Reference for System Components

---

## 1. High-Level System Architecture

```mermaid
C4Context
    title System Context Diagram - SpecHire Platform
    
    Person(hr, "HR Recruiter", "Creates JDs, analyzes CVs, schedules interviews")
    Person(sem, "SE Manager", "Reviews candidates, provides technical feedback")
    Person(admin, "HR Admin", "Views analytics and reports")
    
    System_Boundary(b1, "SpecHire Platform") {
        System(orchestrator, "HR Agent Orchestrator", "Coordinates workflows and manages context")
        System(jd_skill, "JD Analysis SKILL", "Generates and analyzes job descriptions")
        System(cv_skill, "CV Analysis SKILL", "Semantic CV matching and scoring")
    }
    
    System_Ext(llm, "LLM Services", "OpenAI GPT-4, Anthropic Claude")
    System_Ext(job_boards, "Job Boards", "LinkedIn, TopCV, ITviec")
    System_Ext(external, "External APIs", "Salary data, calendar, email")
    
    Rel(hr, orchestrator, "Uses", "HTTPS")
    Rel(sem, orchestrator, "Reviews", "HTTPS")
    Rel(admin, orchestrator, "Views reports", "HTTPS")
    
    Rel(orchestrator, jd_skill, "Invokes")
    Rel(orchestrator, cv_skill, "Invokes")
    
    Rel(jd_skill, llm, "Generates content", "API")
    Rel(cv_skill, llm, "Analyzes CVs", "API")
    Rel(jd_skill, external, "Fetches salary data", "API")
    Rel(orchestrator, job_boards, "Posts jobs", "API")
    Rel(orchestrator, external, "Syncs calendar", "API")
```

---

## 2. Container Architecture

```mermaid
C4Container
    title Container Diagram - SpecHire Internal Architecture
    
    Person(user, "User", "HR/SE Manager")
    
    System_Boundary(c1, "SpecHire Platform") {
        Container(web, "Web Application", "React/Vue", "User interface")
        Container(api, "API Gateway", "FastAPI", "Routes requests, handles auth")
        Container(orchestrator, "HR Agent", "Python", "Coordinates workflows")
        
        Container(jd_skill, "JD SKILL", "Python Service", "Document parsing, JD generation, market analysis")
        Container(cv_skill, "CV SKILL", "Python Service", "CV parsing, fingerprinting, matching")
        
        Container(llm_gw, "LLM Gateway", "Python Service", "Unified LLM access")
        Container(queue, "Message Queue", "RabbitMQ", "Async task processing")
        Container(cache, "Cache", "Redis", "Session & data cache")
        
        ContainerDb(db, "Database", "PostgreSQL + pgvector", "Stores all application data")
        ContainerDb(vector, "Vector DB", "Pinecone", "Semantic search")
        Container(storage, "Object Storage", "S3", "CV files, documents")
    }
    
    System_Ext(llm, "LLM Services", "OpenAI/Anthropic")
    System_Ext(external, "External APIs", "Job boards, calendar, email")
    
    Rel(user, web, "Uses", "HTTPS")
    Rel(web, api, "API calls", "JSON/HTTPS")
    Rel(api, orchestrator, "Routes to", "gRPC")
    
    Rel(orchestrator, jd_skill, "Invokes", "gRPC")
    Rel(orchestrator, cv_skill, "Invokes", "gRPC")
    
    Rel(jd_skill, llm_gw, "Generates", "HTTP")
    Rel(cv_skill, llm_gw, "Analyzes", "HTTP")
    Rel(llm_gw, llm, "API calls", "HTTPS")
    
    Rel(cv_skill, queue, "Publishes jobs", "AMQP")
    Rel(queue, cv_skill, "Processes jobs", "AMQP")
    
    Rel(jd_skill, db, "Reads/Writes", "SQL")
    Rel(cv_skill, db, "Reads/Writes", "SQL")
    Rel(orchestrator, cache, "Caches", "Redis Protocol")
    
    Rel(cv_skill, vector, "Stores embeddings", "API")
    Rel(cv_skill, storage, "Stores CVs", "S3 API")
    
    Rel(orchestrator, external, "Integrates", "REST/OAuth")
```

---

## 3. JD Analysis SKILL - Component Diagram

```mermaid
graph TB
    subgraph "JD Analysis SKILL Service"
        direction TB
        
        A[API Endpoint Layer] --> B[Request Validator]
        
        subgraph "Document Processing"
            B --> C[Document Parser]
            C --> D[Text Extractor]
            D --> E[Requirement Analyzer]
        end
        
        subgraph "Generation Pipeline"
            E --> F[Template Selector]
            F --> G[LLM Generator]
            G --> H[Content Formatter]
        end
        
        subgraph "Intelligence Modules"
            H --> I{Parallel Analysis}
            I --> J[Attract Score<br/>Predictor]
            I --> K[Requirement Gap<br/>Detector]
            I --> L[Bias<br/>Auditor]
            I --> M[Salary<br/>Benchmarker]
        end
        
        subgraph "Output Processing"
            J --> N[Intelligence<br/>Aggregator]
            K --> N
            L --> N
            M --> N
            H --> N
            N --> O[Version<br/>Manager]
            O --> P[Response<br/>Builder]
        end
        
        subgraph "External Integrations"
            Q[LLM API<br/>OpenAI/Claude]
            R[Salary APIs<br/>Glassdoor]
            S[Job Board<br/>Analytics]
        end
        
        subgraph "Data Layer"
            T[(JD Repository)]
            U[(Version History)]
            V[(Cache)]
        end
    end
    
    G -.->|Generate| Q
    M -.->|Fetch| R
    J -.->|Market data| S
    
    P --> T
    O --> U
    N --> V
    
    style J fill:#FFC107
    style K fill:#FFC107
    style L fill:#FFC107
    style M fill:#FFC107
    style G fill:#4CAF50
```

---

## 4. CV Semantic Analysis SKILL - Component Diagram

```mermaid
graph TB
    subgraph "CV Analysis SKILL Service"
        direction TB
        
        A[Batch Upload API] --> B[File Validator]
        B --> C[Queue Manager]
        
        subgraph "Parallel Processing"
            C --> D1[Worker 1]
            C --> D2[Worker 2]
            C --> D3[Worker N]
        end
        
        subgraph "CV Processing Pipeline"
            D1 --> E[Document Parser]
            D2 --> E
            D3 --> E
            E --> F[Structure Extractor]
            F --> G[Entity Recognizer]
        end
        
        subgraph "Depth Fingerprinting"
            G --> H{Orchestrator}
            H --> I[Complexity<br/>Analyzer]
            H --> J[Scale<br/>Analyzer]
            H --> K[Progression<br/>Analyzer]
            H --> L[Consistency<br/>Analyzer]
            
            I --> M[Technical<br/>Fingerprint]
            J --> M
            K --> M
            L --> M
        end
        
        subgraph "Matching Engine"
            M --> N[JD Requirements<br/>Loader]
            N --> O[Semantic<br/>Matcher]
            O --> P[Score<br/>Calculator]
            P --> Q[Auto-<br/>Categorizer]
        end
        
        subgraph "Explainability"
            Q --> R[Why Rejected<br/>Engine]
            R --> S[Blind Spot<br/>Detector]
            S --> T[Explanation<br/>Generator]
        end
        
        subgraph "Results & Learning"
            T --> U[Results<br/>Aggregator]
            U --> V[WebSocket<br/>Progress]
            U --> W[Results DB]
            
            X[Override<br/>Tracker] --> Y[Closed-loop<br/>Learner]
            Y -.->|Retrain| H
        end
        
        subgraph "External"
            Z[LLM API]
            AA[Vector DB]
        end
    end
    
    E -.->|OCR| Z
    I -.->|Analyze| Z
    O -.->|Embeddings| AA
    
    style I fill:#9C27B0
    style J fill:#9C27B0
    style K fill:#9C27B0
    style L fill:#9C27B0
    style R fill:#FF5722
    style S fill:#FF5722
```

---

## 5. Data Flow Diagram - JD Creation Workflow

```mermaid
sequenceDiagram
    actor SEM as SE Manager
    actor HR as HR Recruiter
    participant UI as Web UI
    participant Orch as HR Agent
    participant JD as JD SKILL
    participant LLM as LLM Gateway
    participant Ext as External APIs
    participant DB as Database
    
    SEM->>UI: Upload requirement doc
    UI->>Orch: Create JD request
    Orch->>JD: Invoke JD Generation
    
    activate JD
    JD->>JD: Parse document
    JD->>JD: Extract requirements
    JD->>LLM: Generate JD draft
    LLM-->>JD: Draft content
    
    par Parallel Intelligence Analysis
        JD->>LLM: Calculate Attract Score
        LLM-->>JD: Score + factors
    and
        JD->>JD: Detect requirement gaps
    and
        JD->>JD: Audit bias
    and
        JD->>Ext: Fetch salary benchmark
        Ext-->>JD: Market data
    end
    
    JD->>DB: Save JD draft + analysis
    JD-->>Orch: JD + Intelligence Report
    deactivate JD
    
    Orch-->>UI: Display results
    UI-->>HR: Show draft + recommendations
    
    HR->>UI: Edit & approve
    UI->>Orch: Finalize JD
    Orch->>DB: Update status to "Complete"
    DB-->>Orch: Success
    Orch-->>UI: JD ready for posting
```

---

## 6. Data Flow Diagram - CV Analysis Workflow

```mermaid
sequenceDiagram
    actor HR as HR Recruiter
    participant UI as Web UI
    participant Orch as HR Agent
    participant CV as CV SKILL
    participant Queue as RabbitMQ
    participant Worker as Worker Pool
    participant LLM as LLM Gateway
    participant DB as Database
    participant WS as WebSocket
    
    HR->>UI: Upload 50 CVs
    UI->>Orch: Start batch analysis
    Orch->>CV: Process batch + JD_ID
    
    activate CV
    CV->>Queue: Publish 50 tasks
    CV-->>Orch: Batch accepted
    deactivate CV
    
    Orch-->>UI: Processing started
    UI-->>HR: Show progress bar
    
    loop For each CV
        Queue->>Worker: Dequeue task
        activate Worker
        Worker->>Worker: Parse CV
        Worker->>Worker: Extract structure
        Worker->>Worker: Create fingerprint
        Worker->>LLM: Analyze complexity
        LLM-->>Worker: Analysis
        Worker->>DB: Load JD requirements
        Worker->>Worker: Calculate match score
        Worker->>Worker: Categorize (Q/NR/D)
        Worker->>Worker: Generate explanation
        Worker->>DB: Save result
        Worker->>WS: Update progress
        WS-->>UI: Real-time update
        deactivate Worker
    end
    
    CV->>CV: Aggregate results
    CV->>CV: Detect blind spots
    CV->>DB: Save batch summary
    CV->>WS: Batch complete
    WS-->>UI: Show final results
    
    UI-->>HR: Display dashboard<br/>18 Qualified | 22 Needs Review | 10 Disqualified
    
    HR->>UI: Override CV_003 to Qualified
    UI->>Orch: Record override
    Orch->>CV: Track override
    CV->>DB: Store for learning
```

---

## 7. Deployment Architecture - Kubernetes

```mermaid
graph TB
    subgraph "AWS/GCP Cloud"
        subgraph "Load Balancer"
            A[Application Load Balancer]
        end
        
        subgraph "Kubernetes Cluster - EKS/GKE"
            subgraph "Ingress"
                B[NGINX Ingress Controller]
            end
            
            subgraph "Application Layer"
                C[API Gateway Pods<br/>3 replicas]
                D[HR Agent Pods<br/>3 replicas]
            end
            
            subgraph "SKILL Services"
                E[JD SKILL Pods<br/>3 replicas]
                F[CV SKILL Pods<br/>5 replicas]
            end
            
            subgraph "Workers"
                G[CV Worker Pool<br/>10 replicas<br/>Auto-scaling]
            end
            
            subgraph "Infrastructure"
                H[Redis<br/>Primary + Replica]
                I[RabbitMQ<br/>3-node cluster]
            end
        end
        
        subgraph "Managed Services"
            J[(RDS PostgreSQL<br/>Multi-AZ)]
            K[S3 Buckets<br/>CV Storage]
            L[ElastiCache Redis<br/>Managed]
            M[CloudWatch<br/>Monitoring]
        end
        
        subgraph "External Services"
            N[OpenAI API]
            O[Anthropic API]
            P[Job Board APIs]
        end
    end
    
    A --> B
    B --> C
    C --> D
    D --> E
    D --> F
    F --> G
    G --> I
    E --> H
    F --> H
    C --> J
    E --> J
    F --> J
    F --> K
    E --> L
    F --> L
    
    E -.->|API| N
    F -.->|API| O
    D -.->|API| P
    
    style E fill:#4CAF50
    style F fill:#4CAF50
    style G fill:#FF9800
    style J fill:#2196F3
```

---

## 8. Security Architecture

```mermaid
graph TB
    subgraph "Security Layers"
        subgraph "Edge Protection"
            A[CloudFlare WAF]
            B[DDoS Protection]
            C[Rate Limiting]
        end
        
        subgraph "Network Security"
            D[VPC]
            E[Private Subnets]
            F[Security Groups]
            G[Network ACLs]
        end
        
        subgraph "Application Security"
            H[API Gateway]
            I[JWT Authentication]
            J[RBAC Authorization]
            K[Input Validation]
        end
        
        subgraph "Data Security"
            L[Encryption at Rest<br/>AES-256]
            M[Encryption in Transit<br/>TLS 1.3]
            N[PII Masking]
            O[Database Encryption]
        end
        
        subgraph "Secrets Management"
            P[HashiCorp Vault]
            Q[AWS Secrets Manager]
            R[Key Rotation]
        end
        
        subgraph "Monitoring & Audit"
            S[CloudWatch Logs]
            T[AWS GuardDuty]
            U[Audit Trail]
            V[SIEM Integration]
        end
    end
    
    A --> D
    B --> D
    C --> D
    D --> E
    E --> F
    F --> H
    G --> H
    H --> I
    I --> J
    J --> K
    K --> L
    L --> M
    M --> N
    N --> O
    O --> P
    P --> Q
    Q --> R
    
    H --> S
    D --> T
    J --> U
    S --> V
    T --> V
    U --> V
    
    style A fill:#F44336
    style I fill:#FF9800
    style L fill:#4CAF50
    style P fill:#2196F3
    style V fill:#9C27B0
```

---

## 9. Monitoring Architecture

```mermaid
graph LR
    subgraph "Application Services"
        A[API Gateway]
        B[HR Agent]
        C[JD SKILL]
        D[CV SKILL]
    end
    
    subgraph "Metrics Collection"
        E[Prometheus]
        F[Custom Metrics]
        G[Application Logs]
    end
    
    subgraph "Visualization"
        H[Grafana Dashboards]
        I[Alert Manager]
    end
    
    subgraph "Log Processing"
        J[Fluentd]
        K[Elasticsearch]
        L[Kibana]
    end
    
    subgraph "Tracing"
        M[Jaeger]
        N[OpenTelemetry]
    end
    
    subgraph "Alerting"
        O[PagerDuty]
        P[Slack]
        Q[Email]
    end
    
    A --> E
    B --> E
    C --> E
    D --> E
    
    A --> G
    B --> G
    C --> G
    D --> G
    
    A --> N
    B --> N
    C --> N
    D --> N
    
    E --> F
    F --> H
    H --> I
    
    G --> J
    J --> K
    K --> L
    
    N --> M
    
    I --> O
    I --> P
    I --> Q
    
    style E fill:#FF9800
    style H fill:#4CAF50
    style K fill:#2196F3
    style M fill:#9C27B0
```

---

## 10. CI/CD Pipeline Architecture

```mermaid
graph LR
    subgraph "Development"
        A[Developer<br/>Push Code]
    end
    
    subgraph "Source Control"
        B[GitHub/GitLab]
    end
    
    subgraph "CI Pipeline"
        C[Build]
        D[Unit Tests]
        E[Integration Tests]
        F[Security Scan]
        G[Docker Build]
    end
    
    subgraph "Artifact Storage"
        H[Container Registry<br/>ECR/GCR]
    end
    
    subgraph "CD Pipeline"
        I[Deploy to Dev]
        J[Deploy to Staging]
        K[Approval Gate]
        L[Deploy to Prod]
    end
    
    subgraph "Environments"
        M[Dev Cluster]
        N[Staging Cluster]
        O[Production Cluster]
    end
    
    A --> B
    B -->|Webhook| C
    C --> D
    D --> E
    E --> F
    F --> G
    G --> H
    H --> I
    I --> M
    I --> J
    J --> N
    J --> K
    K -->|Approved| L
    L --> O
    
    style C fill:#4CAF50
    style F fill:#FF9800
    style K fill:#F44336
    style L fill:#2196F3
```

---

## Document Information
- **Version:** 1.0
- **Last Updated:** 2026-03-26
- **Format:** Mermaid Diagrams
- **Purpose:** Visual architecture reference
