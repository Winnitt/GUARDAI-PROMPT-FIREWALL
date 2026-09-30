import base64
import re

ATTACK_PATTERNS = {
    "Instruction Override": [
        r"(?i)ignore\s+(all\s+)?(previous|above)\s+instructions",
        r"(?i)disregard\s+prior\s+prompts",
        r"(?i)system\s+override"
    ],
    "Role Change": [
        r"(?i)you\s+are\s+now\s+in\s+developer\s+mode",
        r"(?i)act\s+as\s+an?\s+unrestricted",
        r"(?i)simulate\s+DAN"
    ],
    "Secret Extraction": [
        r"(?i)reveal\s+(your|the)\s+system\s+prompt",
        r"(?i)print\s+(api\s+key|credentials|secret)",
        r"(?i)output\s+initial\s+instructions"
    ],
    "Tool Abuse": [
        r"(?i)drop\s+table",
        r"(?i)execute\s+command",
        r"(?i)trigger\s+the\s+sql"
    ],
    "Credential Theft": [
        r"(?i)stored\s+user\s+credentials",
        r"(?i)oauth\s+access\s+tokens",
        r"(?i)post\s+them\s+to"
    ],
    "Context Poisoning": [
        r"(?i)from\s+now\s+on,\s+treat\s+all",
        r"(?i)system\s+override\s+note"
    ]
}

def decode_payload(text: str) -> str:
    """Decodes base64 patterns found inside text."""
    b64_matches = re.findall(r'[A-Za-z0-9+/]{20,}==?', text)
    processed = text
    for match in b64_matches:
        try:
            decoded = base64.b64decode(match).decode('utf-8', errors='ignore')
            processed += f"\n[Decoded Payload]: {decoded}"
        except Exception:
            pass
    return processed

def run_heuristic_check(text: str) -> dict:
    processed = decode_payload(text)
    detected = []
    
    # Check if encoded instruction was present
    if "[Decoded Payload]:" in processed:
        detected.append("Encoded Instructions")

    for attack_type, patterns in ATTACK_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, processed):
                if attack_type not in detected:
                    detected.append(attack_type)
                break
                
    return {
        "is_safe": len(detected) == 0,
        "threats": detected,
        "processed_text": processed
    }