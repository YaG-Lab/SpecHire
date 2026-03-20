# Introduction & Overview

## Overview

The recruitment process involves a clear division of roles between the **Recruiter (HR)**, **Hiring Admin (HR Manager)**, and **SE Manager (Department Head - IT, Marketing, etc.)**.

```plaintext
HR <--Basic Criteria Screening--> HR Admin <--Detailed Discussion & Evaluation--> SE Manager
```

A Recruiter's tasks consist of two main groups:

### 1. Recruitment Operations (Demand-driven)

Steps taken when departments request additional personnel:

- **Job Description (JD) Preparation:**
  - HR does not create JDs from scratch; they are provided by Department Heads.
  - HR typically reuses existing JD templates, updating them only if there are significant changes in technology or management requirements.
- **Basic Screening:**
  - **Hard Criteria:** Filters based on surface information: Degrees, years of experience, age, gender, field of study, and geographical distance (commute).
  - **Basic Keyword Matching:** 1-to-1 matching. For example, if Python and C++ are required, HR looks specifically for "Python" and "C++" in the CV. HR usually cannot assess project depth or technological adaptability.
- **Shortlisting & Coordination:**
  - If there are too many qualified CVs (e.g., 20), HR selects a set number (e.g., 10) based on hard criteria.
  - This list is forwarded to the Hiring Manager for deep technical evaluation (IT expertise, real-world projects).
- **Interview Coordination:**
  - Once the Manager selects candidates, HR handles contacting and scheduling interviews (via phone or in-person).

### 2. HR Administrative Operations (HR Admin/C&B - Main workload)

Outside of recruitment cycles, HR's time is primarily dedicated to C&B (Compensation & Benefits) and internal operations:

- **Attendance & Payroll:** Tracking workdays, leave, and attendance records.
- **Personnel Records Management:** Managing labor contracts, onboarding new hires, and processing offboarding procedures.
- **Insurance & Benefits:** Handling Social Insurance (BHXH), Health Insurance (BHYT), and other employee welfare programs.

## Project Objectives

The core issue is the gap between HR's basic screening capability and the SE Manager's deep technical requirements, leading to time wasted on irrelevant CVs or missing talent due to precise keyword mismatches. This AI Agent is built with the following goals:

- **Automate Job Posting on Recruitment Platforms**: Reduce time spent writing and posting job advertisements on social groups and hiring platforms.
- **Automate the Initial Screening Funnel:** Reduce HR manual screening time by 80% through automated CV parsing and evaluation.
- **Enhance Shortlist Quality:** Move from "1-to-1 keyword matching" to "semantic understanding" (Semantic Matching via NLP) to accurately assess core competencies relative to the JD.
- **Decision Support for SE Managers:** Provide Matching Scores and AI-generated summaries for each candidate, enabling Managers to make faster interview decisions.
- **Human Resource Optimization:** Free up recruitment time for HR to focus on C&B, onboarding, and employee experience management.

## Scope

Defining system boundaries is essential to prevent "Scope Creep" during development.

**In-scope:**

- AI generating structured Job Descriptions (JDs) from SE Manager requirements.
- Automated job posting via platform integrations.
- Allowing HR to upload batch CVs (PDF, Word formats).
- AI Agent parsing CV data and using Large Language Models (LLM) to extract entities and analyze context relative to JD requirements.
- Automated Scoring and categorization of CVs into: Qualified, Needs Review, Disqualified.
- Dashboard displaying detailed evaluation reports (AI Reasoning) for each candidate for HR and SE Manager review.
- Interview coordination syncing with Google Calendar and automated rejection emails.
- Implementation of Human-In-The-Loop (HITL) framework at critical decision points.

**Out-of-scope:**

- Technical skill testing (Coding tests, IQ/EQ tests) are explicitly out-of-scope and processed externally.
- Final hiring decisions (Decision strictly remains with humans).
- HR Admin, payroll, or attendance management.

## Glossary & Key Concepts

- **Human-In-The-Loop (HITL):** A core design principle of this system where AI assists rather than replaces human decision-making. AI acts as an advisor, and humans retain full control at critical checkpoints:
  - **JD Approval:** HR must manually review, edit, and approve AI-generated Job Descriptions before they can be posted (Module 2).
  - **CV Shortlist Finalization:** HR reviews AI scores, can override categorization labels, and manually forwards the final list to the SE Manager (Module 4).
  - **Final Hiring Decisions:** AI matching scores are for reference; SE Managers evaluate AI reasoning and make the ultimate decision to interview or hire.
  - **Communication:** Rejections and interview schedules are drafted/prompted by AI but executed by humans (Module 5).

## Stakeholders

List of Actors interacting directly or indirectly with the AI Agent system:

- **HR / Recruiter (Primary User):** Uploads JDs/CVs and receives AI-scored/filtered lists to forward to Department Heads.
- **SE Manager / Hiring Manager (Beneficiary):** Receives shortlists with AI-generated technical summaries to decide whom to interview.
- **Hiring Admin / HR Manager (Administrator):** Monitors high-level metrics (Analytics) such as Time-to-hire and CV-to-interview conversion rates to evaluate AI Agent effectiveness.
- **System Admin / IT Support:** Responsible for configuration, prompt tuning, AI parameters, and ensuring stable data extraction.
