# 🛡️ GuardAI: Enterprise Prompt Injection Firewall

> **ET AI Hackathon: Agentic Edition** | *Problem 2: Agentic Cybersecurity - Prompt Injection Firewall*  
> **Target Matrix Positioning:** **F3** (Feature Coverage) | **D2** (Solution Depth)

GuardAI is a dual-tier, zero-trust security gateway engineered to intercept, analyze, and neutralize prompt injection attacks targeting LLM agents, copilots, and autonomous tools across multi-format input data.

---

## 🚀 Key Features & Attack Vector Coverage (Target: F3)

GuardAI intercepts all incoming traffic before it reaches downstream AI models, detecting over **9 distinct attack categories**:

1. **Instruction Override:** Direct attempts to subvert initial system prompts.
2. **Role Change / Jailbreaks:** Persona shifts (e.g., DAN, Developer Mode) bypassing safety filters.
3. **Secret Extraction:** Leaking hidden instructions, system prompts, or embedded API keys.
4. **Tool Abuse:** Executing unauthorized database or OS-level commands (e.g., SQL injection, shell scripts).
5. **Credential Theft:** Extracting session tokens, passwords, or authorization credentials.
6. **Context Poisoning:** Manipulating memory banks or long-context data streams.
7. **Multi-Step Jailbreaks:** Complex multi-turn or hypothetical roleplay exploit triggers.
8. **Encoded Instructions:** Obfuscated attack payloads utilizing Base64 or Hex encoding.
9. **Indirect Prompt Injection:** Hidden malicious instructions inside external content (emails, web scrapes, PDFs).

---

## 🏗 Technical Architecture & Dual-Tier Defense