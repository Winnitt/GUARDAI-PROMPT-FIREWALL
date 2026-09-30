# GuardAI: Enterprise Prompt Injection Firewall

> **ET AI Hackathon: Agentic Edition**  
> **Problem 2: Agentic Cybersecurity - Prompt Injection Firewall**

> **Target Matrix Positioning:**  
> **F3 (Feature Coverage)** | **D2 (Solution Depth)**

---

## Overview

GuardAI is a dual-tier, zero-trust security gateway engineered to intercept, analyze, and neutralize prompt injection attacks targeting LLM agents, copilots, and autonomous AI systems across multi-format input sources.

The system acts as a security layer between incoming user/external data and downstream AI models, ensuring that malicious instructions, hidden payloads, and adversarial behaviors are detected before reaching AI agents.

---

# Key Features and Attack Vector Coverage

GuardAI provides comprehensive protection against **9 major prompt injection attack categories**:

## 1. Instruction Override

Detects attempts to bypass or replace original system instructions through malicious user prompts.

Example:
- "Ignore previous instructions and follow my commands."

---

## 2. Role Change and Jailbreak Attacks

Identifies persona manipulation attempts designed to bypass AI safety mechanisms.

Examples:
- DAN attacks
- Developer mode exploits
- Unauthorized role switching

---

## 3. Secret Extraction

Detects attempts to reveal:

- System prompts
- Hidden instructions
- API keys
- Internal configurations

---

## 4. Tool Abuse

Prevents unauthorized execution or manipulation of external tools.

Examples:

- SQL injection attempts
- Shell command execution
- Database manipulation requests

---

## 5. Credential Theft

Identifies attempts to extract sensitive authentication information:

- Passwords
- Access tokens
- Session credentials
- Authorization headers

---

## 6. Context Poisoning

Detects malicious modifications to:

- Long-term memory
- Retrieved context
- Knowledge sources
- Agent state

---

## 7. Multi-Step Jailbreaks

Analyzes complex attack chains involving:

- Multi-turn conversations
- Roleplay exploits
- Gradual instruction manipulation

---

## 8. Encoded Instructions

Detects hidden malicious instructions using:

- Base64 encoding
- Hex encoding
- Obfuscated payloads

---

## 9. Indirect Prompt Injection

Identifies hidden instructions embedded inside external content:

- Emails
- PDFs
- HTML pages
- Web documents
- Retrieved knowledge sources

---

# Technical Architecture and Dual-Tier Defense


```
Incoming Payload
        |
        v
Preprocessor and Decoder Layer
        |
        v
+-------------------------------+
| Tier 1: Local Heuristic Engine |
+-------------------------------+
        |
        | Static Threat Match
        |
        +-------------> BLOCK
        |
        v
+--------------------------------+
| Tier 2: Agentic Intent Inspector |
|          Gemini 2.5 Flash       |
+--------------------------------+
        |
        | Semantic Threat Analysis
        |
        +-------------> BLOCK
        |
        v
Dispatch to LLM Agent
```

---

# Core Components

## Data Preprocessor (`engine/preprocessor.py`)

Responsible for:

- Extracting text from heterogeneous sources
- Supporting PDF, HTML, and TXT inputs
- Detecting and decoding encoded payloads
- Normalizing incoming data streams

---

## Tier 1: Local Heuristic Engine (`engine/heuristics.py`)

A lightweight, zero-latency security layer using:

- Regex pattern matching
- Static attack signatures
- Encoding detection
- System prompt leakage detection
- SQL and command injection patterns

Purpose:

- Fast threat detection
- Immediate blocking of known attacks

---

## Tier 2: Agentic Intent Inspector (`engine/intent_checker.py`)

Powered by **Gemini 2.5 Flash**, this layer performs semantic reasoning to detect:

- Indirect prompt injection
- Context manipulation
- Tool misuse attempts
- Advanced jailbreak strategies
- Multi-step attack patterns

Purpose:

- Detect unknown and context-based attacks
- Analyze attacker intent beyond keywords

---

## Security Operations Console (`app.py`)

A Streamlit-based enterprise SOC dashboard providing:

- Real-time threat analysis
- Risk scoring
- Attack categorization
- Firewall decision reporting
- Security event logging

The interface follows modern enterprise security dashboard principles inspired by platforms such as CrowdStrike Falcon and Palo Alto Cortex.

---

# Installation and Setup

## Prerequisites

Required:

- Python 3.10+
- Google AI Studio Gemini API Key

---

# Setup Instructions

## 1. Clone Repository

```bash
git clone https://github.com/Winnitt/GUARDAI-PROMPT-FIREWALL.git

cd GUARDAI-PROMPT-FIREWALL
```

---

## 2. Create Virtual Environment

### Windows (PowerShell)

```powershell
python -m venv venv

venv\Scripts\activate
```

### macOS/Linux

```bash
python -m venv venv

source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

---

## 5. Launch Security Operations Dashboard

Run:

```bash
streamlit run app.py
```

---

# Security Workflow

1. User or external system submits input payload.
2. GuardAI extracts and preprocesses the content.
3. Encoded or obfuscated payloads are decoded.
4. Tier 1 heuristic analysis performs fast detection.
5. Suspicious inputs are blocked immediately.
6. Ambiguous inputs are analyzed by Gemini-powered intent inspection.
7. Safe requests are forwarded to the target AI agent.
8. Threat events are logged for security monitoring.

---

# Project Goal

GuardAI enables secure deployment of autonomous AI systems by providing a zero-trust security gateway that protects LLM applications from evolving prompt injection attacks.