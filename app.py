import streamlit as st
import json
from dotenv import load_dotenv
from engine.preprocessor import extract_text_from_file, decode_obfuscated_payloads
from engine.heuristics import run_heuristic_check
from engine.intent_checker import analyze_intent

load_dotenv()

# Page configuration with dark theme setup
st.set_page_config(
    page_title="GuardAI | Cortex SOC Gateway",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for CrowdStrike / Palo Alto SOC styling
st.markdown("""
<style>
    /* Dark Theme Base Overrides */
    .stApp {
        background-color: #0d1117;
        color: #c9d1d9;
    }
    
    /* Header Styling */
    .soc-header {
        border-bottom: 2px solid #30363d;
        padding-bottom: 12px;
        margin-bottom: 20px;
    }
    .soc-title {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #58a6ff;
        font-weight: 700;
        letter-spacing: 0.5px;
        font-size: 28px;
        margin: 0;
    }
    .soc-subtitle {
        color: #8b949e;
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 1.2px;
    }

    /* Metric Cards */
    div[data-testid="stMetric"] {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 12px 16px;
        border-radius: 6px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    div[data-testid="stMetricLabel"] {
        color: #8b949e !important;
        font-size: 12px !important;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }
    div[data-testid="stMetricValue"] {
        font-size: 20px !important;
        font-weight: 600 !important;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #30363d;
    }

    /* Custom Threat Box Containers */
    .threat-box-safe {
        background-color: rgba(46, 160, 67, 0.1);
        border: 1px solid #2ea043;
        padding: 16px;
        border-radius: 6px;
        margin-bottom: 12px;
    }
    .threat-box-danger {
        background-color: rgba(248, 81, 73, 0.1);
        border: 1px solid #f85149;
        padding: 16px;
        border-radius: 6px;
        margin-bottom: 12px;
    }
    .threat-title {
        font-weight: 600;
        font-size: 15px;
        margin-bottom: 6px;
    }
</style>
""", unsafe_allow_html=True)

# Top Bar / SOC Brand Header
st.markdown("""
<div class="soc-header">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <div class="soc-title">🛡️ GUARDAI PROMPT FIREWALL</div>
            <div class="soc-subtitle">Zero-Trust LLM Gateway & Real-Time Threat Mitigation System</div>
        </div>
        <div style="text-align: right;">
            <span style="background-color: #238636; color: white; padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: bold;">
                SYSTEM ONLINE
            </span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar - Threat Simulation Console
st.sidebar.markdown("###  THREAT SIMULATOR CONSOLE")
st.sidebar.caption("Select a pre-configured vector or submit a raw payload:")

try:
    with open("data/test_samples.json", "r") as f:
        samples = json.load(f)
    sample_titles = ["-- Select Attack Vector --"] + [s["title"] for s in samples]
    selected_sample = st.sidebar.selectbox("Attack Profiles:", sample_titles)
except Exception:
    samples = []
    selected_sample = "-- Select Attack Vector --"

default_text = ""
if selected_sample != "-- Select Attack Vector --":
    for s in samples:
        if s["title"] == selected_sample:
            default_text = s["content"]

st.sidebar.divider()
st.sidebar.markdown("### ⚙️ GATEWAY CONFIGURATION")
st.sidebar.text("Policy: Strict Block")
st.sidebar.text("Inspection Mode: Dual-Tier")
st.sidebar.text("Telemetry: Active SIEM Feed")

# Input Processing Panel
input_type = st.radio("Ingress Vector:", ["Text / Prompt Payload", "Document Stream (PDF / HTML / TXT)"], horizontal=True)

input_content = ""

if input_type == "Text / Prompt Payload":
    input_content = st.text_area("Ingress Data Stream:", value=default_text, height=140, placeholder="Paste user prompt, email payload, or raw API text stream...")
else:
    uploaded_file = st.file_uploader("Upload External Content Payload", type=["pdf", "html", "txt"])
    if uploaded_file:
        file_bytes = uploaded_file.read()
        input_content = extract_text_from_file(file_bytes, uploaded_file.name)
        st.text_area("Parsed Ingress Stream:", value=input_content[:600] + ("..." if len(input_content) > 600 else ""), height=120)

st.divider()

# Execute Scan Button
if st.button(" EXECUTE  THREAT SCAN", type="primary", use_container_width=True):
    if not input_content.strip():
        st.warning("⚠️ No ingress payload detected for inspection.")
    else:
        # Preprocessing & Obfuscation Extraction
        decoded_text = decode_obfuscated_payloads(input_content)
        
        # Execute Inspection Tiers
        heuristic_res = run_heuristic_check(decoded_text)
        
        with st.spinner("🔍 Agentic SOC Engine inspecting payload semantics..."):
            intent_res = analyze_intent(decoded_text)
            
        is_overall_safe = heuristic_res["is_safe"] and intent_res["is_safe"]
        risk_score = max(0 if heuristic_res["is_safe"] else 85, intent_res.get("risk_score", 0))

        # SOC Executive Status Dashboard
        m1, m2, m3, m4 = st.columns(4)
        
        if is_overall_safe:
            m1.metric("DISPOSITION", "CLEARED 🟢")
            m2.metric("THREAT SEVERITY", f"{risk_score} / 100", delta="LOW RISK", delta_color="normal")
        else:
            m1.metric("DISPOSITION", "BLOCKED 🔴")
            m2.metric("THREAT SEVERITY", f"{risk_score} / 100", delta="HIGH RISK", delta_color="inverse")
            
        m3.metric("TIER 1 (HEURISTICS)", "PASS" if heuristic_res["is_safe"] else "VIOLATION")
        m4.metric("TIER 2 (AGENTIC INTENT)", "PASS" if intent_res["is_safe"] else "VIOLATION")

        st.markdown("<br>", unsafe_allow_html=True)

        # Detailed Tier Breakdown
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### ⚡ Tier 1: Static Heuristic Inspection")
            if heuristic_res["is_safe"]:
                st.markdown("""
                <div class="threat-box-safe">
                    <div class="threat-title" style="color: #2ea043;">✅ NO STATIC VIOLATIONS</div>
                    <div style="font-size: 13px; color: #8b949e;">Pattern rules and obfuscation checks passed without triggering static security signatures.</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                threats_str = ", ".join(heuristic_res['threats'])
                st.markdown(f"""
                <div class="threat-box-danger">
                    <div class="threat-title" style="color: #f85149;">❌ STATIC VIOLATION DETECTED</div>
                    <div style="font-size: 13px; color: #c9d1d9;"><b>Categories Flagged:</b> {threats_str}</div>
                    <div style="font-size: 12px; color: #8b949e; margin-top: 4px;">Matched signature rules or base64 payload overrides.</div>
                </div>
                """, unsafe_allow_html=True)

        with col2:
            st.markdown("#### 🤖 Tier 2: Agentic Intent Analysis")
            if intent_res["is_safe"]:
                st.markdown("""
                <div class="threat-box-safe">
                    <div class="threat-title" style="color: #2ea043;">✅ NO SEMANTIC THREATS</div>
                    <div style="font-size: 13px; color: #8b949e;">Gemini Agentic Inspector verified clean intent. No indirect injection or jailbreaks identified.</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                threats_str = ", ".join(intent_res.get('threats', ['Malicious Intent']))
                reasoning_str = intent_res.get('reasoning', 'Subtle prompt subversion detected.')
                st.markdown(f"""
                <div class="threat-box-danger">
                    <div class="threat-title" style="color: #f85149;">❌ SEMANTIC THREAT DETECTED</div>
                    <div style="font-size: 13px; color: #c9d1d9;"><b>Categories Flagged:</b> {threats_str}</div>
                    <div style="font-size: 12px; color: #8b949e; margin-top: 4px;"><b>Analysis:</b> {reasoning_str}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Executive Mitigation Log
        st.markdown("#### 📋 SIEM Event Log & Dispatch Response")
        if is_overall_safe:
            st.success("🟢 PAYLOAD SANITIZED & DISPATCHED TO DOWNSTREAM AGENT")
            st.json({
                "event_id": "EVT-884920",
                "action": "FORWARD_TO_MODEL",
                "risk_level": "LOW",
                "ingress_payload": input_content,
                "mitigation": "None required. Payload passed all inspection gates."
            })
        else:
            st.error("🔴 INGRESS PAYLOAD DROPPED & SECURITY EVENT LOGGED")
            all_threats = list(set(heuristic_res["threats"] + intent_res.get("threats", [])))
            st.json({
                "event_id": "EVT-992104",
                "action": "BLOCK_AND_NEUTRALIZE",
                "risk_score": risk_score,
                "threat_categories": all_threats,
                "mitigation": "Payload terminated at ingress gate. Alert broadcasted to SOC SIEM console."
            })