# Business Processes

This section outlines how the recruitment workflow operates, contrasting the current manual state with the automated process enabled by the AI Agent.

## Filter CV Processes

### Current Process (As-is)

The existing workflow is heavily manual and relies on simple keyword matching, often leading to inefficiencies or missed talent.

1.  **JD Preparation**: HR receives talent requirements from the SE Manager and prepares the Job Description, usually by updating existing templates.
2.  **Sourcing**: HR posts the JD on various job boards and collects CVs.
3.  **Basic Screening (Manual)**: HR manually filters hundreds of CVs based on:
    - **Hard Criteria**: Location, age, degree, and years of experience.
    - **Basic Keyword Matching**: Searching for specific terms (e.g., "React", "Python") without understanding the candidate's actual proficiency or project context.
4.  **Initial Shortlisting**: HR selects a broad list (e.g., 20 candidates) based on these surface-level filters.
5.  **Technical Review**: The list is sent to the SE Manager, who must spend time reviewing candidates that may not actually have the required technical depth.
6.  **Interview Coordination**: HR contacts the selected candidates to schedule interviews
    - Behavior Interview, using STAR technique (Situation, Task, Action, Result)
    - Assessment Tests: Cognitive Ability Tests, Work Sample Tests / Coding Tests, Personality Assessments.
    - Cultural Fit / Value Fit

**Pain Points**: High workload for HR, inconsistent screening quality, and "keyword matching" gaps that frustrate technical managers.

```mermaid
flowchart TD
    S([Start]) --> A[Receive Hiring Request HR receives from SE Manager]
    A --> B[Draft Job Description Update from existing templates]
    B --> C[Post JD to Job Boards LinkedIn, TopCV, ITviec…]
    C --> D[Collect Candidate CVs]
    D --> F1{Fork}
    F1 --> E1[Filter Hard Criteria Location, Age, Degree]
    F1 --> E2[Keyword Matching Search: React, Python…]
    E1 --> J1{Join}
    E2 --> J1
    J1 --> G{Meet Hard Criteria?}
    G -- No --> X1([Reject CV])
    G -- Yes --> H[Initial Shortlisting]
    H --> I[SE Manager Review CV Technical Depth Evaluation]
    I --> K{Meet Technical Requirements?}
    K -- No --> X2([Reject CV])
    K -- Yes --> L[HR Coordinates Interviews]
    L --> F2{Fork}
    F2 --> M1[Behavioral Interview STAR Technique]
    F2 --> M2[Assessment Tests Cognitive, Coding Test]
    F2 --> M3[Culture Evaluation Cultural / Value Fit]
    M1 --> J2{Join}
    M2 --> J2
    M3 --> J2
    J2 --> N[Synthesize Results & Offer Hiring Decision]
    N --> E([End])
```

### Desired Process (To-be)

The AI Agent transforms the process by introducing semantic understanding, automated JD generation, and streamlined workflows across all modules.

1.  **JD Generation (Module 2)**: SE Manager uploads hiring requirements. The AI Agent automatically drafts a structured Job Description (JD). HR reviews, edits, and approves the final JD (HITL).
2.  **Automated Job Posting (Module 3)**: HR selects recruitment platforms, and the system automatically posts the approved JD.
3.  **CV Input (Module 4)**: HR uploads batch CVs into the AI Agent system for the specific JD.
4.  **Automated Extraction**: The AI Agent identifies mandatory skills, experience levels, and preferred qualifications from the JD.
5.  **Semantic Evaluation (AI-Driven)**:
    - **Parsing**: The LLM extracts education, work history, and project details from CVs.
    - **Matching**: Instead of counting keywords, the AI analyzes the "depth" of experience and alignment with JD requirements.
    - **Scoring & Reasoning**: The AI generates a **Matching Score** and a short summary of **AI Reasoning** (pros/cons) for each candidate.
6.  **Ranked Dashboard (Module 4)**: HR reviews a ranked list of candidates on a dashboard, adjusting classifications if needed (HITL).
7.  **Manager Collaboration**: The SE Manager accesses the system to review the HR-forwarded shortlist, focusing only on the most qualified candidates with the help of AI summaries.
8.  **Rejection & Interview Coordination (Module 5)**:
    - HR triggers automated rejection emails for non-matching candidates.
    - HR schedules interviews, which sync with Google Calendar, and the AI provides appropriate Call Scripts. _(Note: Technical skill tests like coding tests are handled externally and not integrated into this system)._
9.  **Analytics & Reporting (Module 7)**: Hiring Admins review dashboards tracking conversion rates, AI effectiveness, and average Time-to-hire.

### Activity Diagram

The following diagram illustrates the interaction between the stakeholders and the AI Agent across all modules.

```mermaid
flowchart TD
    subgraph HR["HR / Recruiter"]
        A2[Review & Approve Draft JD]
        B[Automated Job Posting]
        B2[Upload Batch CVs]
        G[Review Dashboard Rankings]
        H{Need Clarification?}
        I[Review AI Reasoning]
        J[Finalize Shortlist & Forward]
        L[Coordinate Interviews]
        M[Send Rejection Emails]
    end

    subgraph AI["AI Agent"]
        A1[Draft JD from Requirements]
        C[Extract JD & CV Entities]
        E[Semantic Matching & Scoring]
        F[Generate AI Reasoning]
        L1[Sync Calendar & Generate Scripts]
    end

    subgraph SE["SE Manager"]
        A([Start: Upload Requirements])
        K[Review Technical Summaries & Select for Interview]
    end

    A --> A1
    A1 --> A2
    A2 --> B
    B --> B2
    B2 --> C
    C --> E
    E --> F
    F --> G
    G --> H
    H -- Yes --> I
    I --> J
    H -- No --> J
    J --> K
    K --> L
    K --> M
    L --> L1
    L1 --> N([End])
    M --> N
```

## Tracking and Evaluating Personnel

### Evaluation Criteria Frameworks:

1. **Core Competency Criteria (ASK / KSAO Model)**
   This is the most fundamental criteria framework to assess whether an individual is capable of performing the job.

- **Knowledge**: The understanding of theory, professional expertise, and processes. In IT, this includes knowledge of data structures, algorithms, and programming languages.

- **Skills**: The ability to apply knowledge into practice to generate results. Examples: Clean code writing skills, ability to use version control tools (Git).

- **Abilities / Attitude**: Cognitive capacity, logical reasoning, willingness to learn, discipline, and perseverance. Unlike skills that can be learned quickly, abilities and attitudes are more enduring characteristics of an individual.

2. **Performance Criteria (Task vs. Contextual Performance)**
   When evaluating personnel (especially current employees or candidates through practical tests), behavioral psychology theory divides performance into two types:

- **Task Performance**: Evaluates the completion level of tasks explicitly stated in the Job Description (JD). This criterion is often measured by quantity (number of bugs fixed, lines of code) and quality (system optimization level, defect rate). It is typically quantified through KPIs (Key Performance Indicators) or OKRs (Objectives and Key Results) systems.

- **Contextual Performance**: Evaluates behaviors not listed in the JD but that contribute to the psychological and social environment of the organization. Criteria include: proactiveness in helping colleagues, willingness to take on additional tasks, and ability to collaborate (Teamwork).

3. **Person-Organization Fit (P-O Fit) Criteria**
   This is the decisive criterion for whether an employee will stay long-term and maximize their potential at the company.

- **Value Congruence**: Evaluates whether the individual's beliefs and working style align with the company culture (e.g., an individual prefers safety and stability vs. a company that demands innovation and risk-taking).

- **Long-term Goals**: Whether the individual's career destination is aligned with the organization's development roadmap.

### Current Process (As-is)

Currently, tracking and evaluating personnel during probation relies heavily on manual observation and sporadic feedback.
1. **Manual Tracking**: The SE Manager informally observes the candidate's performance and behavior.
2. **Infrequent Feedback**: Feedback is typically given only at the end of the probation period or when critical issues arise.
3. **Subjective Evaluation**: Decisions to pass or fail probation often rely on subjective impressions rather than a structured, data-driven framework.

**Pain Points**: High risk of bias, lack of continuous feedback for candidate improvement, and difficulty for HR to track probation progress holistically.

### Desired Process (To-be)

The AI Agent digitizes and enhances the probation evaluation process by enabling continuous tracking, structured frameworks, and data-driven analytics.
1. **Continuous Input**: The SE Manager regularly logs evaluations and feedback into the system based on the ASK, Performance, and P-O Fit frameworks.
2. **AI Analysis**: The AI Agent continuously monitors these inputs, analyzing task performance, contextual behaviors, and cultural alignment.
3. **Advanced Analytics**: The system utilizes advanced analytics to generate detailed insights, scoring the candidate's performance and providing actionable guidance to the manager.
4. **Comprehensive Reporting**: HR Managers and SE Managers access real-time dashboards and exportable reports to make informed, objective decisions about the candidate's probation outcome (HITL).

### Activity Diagram

The following diagram illustrates the interaction between the stakeholders and the AI Agent during the Probation Tracking & Evaluation phase.

```mermaid
flowchart TD
    subgraph HR["HR Manager"]
        D[Review Analytics Dashboard & Reports]
        F[Finalize Probation Decision]
    end

    subgraph AI["AI Agent"]
        C[Analyze Inputs & Generate Advanced Analytics]
    end

    subgraph SE["SE Manager"]
        A([Start: Probation Period])
        B[Log Continuous Evaluations ASK, Performance, P-O Fit]
        E[Review AI Insights & Guidance]
    end

    A --> B
    B --> C
    C --> D
    C --> E
    E --> F
    D --> F
    F --> G([End: Probation Outcome])
```
