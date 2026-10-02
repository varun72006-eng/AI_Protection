# ==========================================
# SIMPLE AI SAFETY SCANNER
# ==========================================


def scan_prompt(prompt):

    # Prompt ko lowercase me convert kar rahe hain
    prompt = prompt.lower()

    # ------------------------------------------
    # 1. JAILBREAK CHECK
    # ------------------------------------------

    if "ignore previous instructions" in prompt:
        return {
            "status": "UNSAFE",
            "risk_score": 90,
            "attack": "Jailbreak",
            "message": "Jailbreak attack detected"
        }

    if "ignore all previous instructions" in prompt:
        return {
            "status": "UNSAFE",
            "risk_score": 90,
            "attack": "Jailbreak",
            "message": "Jailbreak attack detected"
        }

    if "bypass safety" in prompt:
        return {
            "status": "UNSAFE",
            "risk_score": 90,
            "attack": "Jailbreak",
            "message": "Jailbreak attack detected"
        }

    # ------------------------------------------
    # 2. PROMPT INJECTION CHECK
    # ------------------------------------------

    if "system prompt" in prompt:
        return {
            "status": "UNSAFE",
            "risk_score": 90,
            "attack": "Prompt Injection",
            "message": "Prompt injection detected"
        }

    if "reveal your instructions" in prompt:
        return {
            "status": "UNSAFE",
            "risk_score": 90,
            "attack": "Prompt Injection",
            "message": "Prompt injection detected"
        }

    if "show your instructions" in prompt:
        return {
            "status": "UNSAFE",
            "risk_score": 90,
            "attack": "Prompt Injection",
            "message": "Prompt injection detected"
        }

    # ------------------------------------------
    # 3. ROLE PLAY ATTACK CHECK
    # ------------------------------------------

    if "act as an unrestricted ai" in prompt:
        return {
            "status": "UNSAFE",
            "risk_score": 90,
            "attack": "Role Play Attack",
            "message": "Role-play attack detected"
        }

    if "act as an uncensored ai" in prompt:
        return {
            "status": "UNSAFE",
            "risk_score": 90,
            "attack": "Role Play Attack",
            "message": "Role-play attack detected"
        }

    # ------------------------------------------
    # 4. SAFE PROMPT
    # ------------------------------------------

    return {
        "status": "SAFE",
        "risk_score": 5,
        "attack": "None",
        "message": "No known attack pattern detected"
    }