import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.services.gemini_service import generate_ai_response
from backend.services.safety_scanner import scan_prompt
from backend.services.hallucination_checker import check_hallucination


app = FastAPI(title="SafeGuard AI")


# ==========================================
# CORS
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# REQUEST MODEL
# ==========================================

class PromptRequest(BaseModel):
    prompt: str


# ==========================================
# HOME
# ==========================================

@app.get("/")
def home():

    return {
        "message": "SafeGuard AI Backend is Running!"
    }


# ==========================================
# ASK AI
# ==========================================

@app.post("/ask")
def ask_ai(request: PromptRequest):

    start_time = time.time()

    prompt = request.prompt


    # ======================================
    # SAFETY SCAN
    # ======================================

    safety_result = scan_prompt(prompt)


    # ======================================
    # BLOCK UNSAFE PROMPT
    # ======================================

    if safety_result["status"] == "UNSAFE":

        total_time = round(
            (time.time() - start_time) * 1000,
            2
        )

        return {

            "status": "BLOCKED",

            "safety": safety_result,

            "response":
                "This prompt was blocked because it appears to contain unsafe instructions.",

            "hallucination": None,

            "latency": {
                "total_ms": total_time,
                "llm_called": False
            }

        }


    # ======================================
    # SAFE → CALL GEMINI
    # ======================================

    try:

        response = generate_ai_response(
            safety_result["sanitized_prompt"]
        )

    except Exception as error:

        total_time = round(
            (time.time() - start_time) * 1000,
            2
        )

        return {

            "status": "ERROR",

            "safety": safety_result,

            "response":
                "AI service is currently unavailable. Please try again later.",

            "hallucination": None,

            "latency": {
                "total_ms": total_time,
                "llm_called": True
            },

            "error": str(error)

        }


    # ======================================
    # HALLUCINATION CHECK
    # ======================================

    hallucination_result = check_hallucination(
        prompt,
        response
    )


    # ======================================
    # TOTAL LATENCY
    # ======================================

    total_time = round(
        (time.time() - start_time) * 1000,
        2
    )


    # ======================================
    # FINAL SAFETY REPORT
    # ======================================

    return {

        "status": "SAFE",

        "safety": safety_result,

        "response": response,

        "hallucination": hallucination_result,

        "latency": {

            "total_ms": total_time,

            "llm_called": True

        }

    }