import os
import json
import requests
import traceback
from openai import OpenAI

# --- Env vars: match exactly what the hackathon injects ---
# API_BASE_URL may or may not have /v1 suffix — we normalise it
_raw_base = os.environ.get("API_BASE_URL", "https://router.huggingface.co/v1")
API_BASE_URL = _raw_base.rstrip("/")
if not API_BASE_URL.endswith("/v1"):
    API_BASE_URL = API_BASE_URL + "/v1"

# Hackathon injects API_KEY or HF_TOKEN — accept either
API_KEY = os.environ.get("API_KEY") or os.environ.get("HF_TOKEN", "")

# Model: use what they inject, fallback to a known working HF model
MODEL_NAME = os.environ.get("MODEL_NAME", "openai/gpt-oss-120b:novita")

SPACE_URL = os.environ.get("SPACE_URL", "https://samm14-email-management-openenv.hf.space")

print(f"[DEBUG] API_BASE_URL = {API_BASE_URL}")
print(f"[DEBUG] API_KEY present = {bool(API_KEY)}, length = {len(API_KEY)}")
print(f"[DEBUG] MODEL_NAME = {MODEL_NAME}")
print(f"[DEBUG] SPACE_URL = {SPACE_URL}")

# Build client exactly like the official OpenEnv examples
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=API_KEY,
)


def call_llm(prompt: str) -> str:
    """Call LLM through hackathon proxy"""
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are an email assistant. Respond with valid JSON only. No markdown."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.3,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[DEBUG] call_llm error: {type(e).__name__}: {e}")
        print(traceback.format_exc())
        raise


def parse_action(text: str) -> dict:
    text = text.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        text = "\n".join(lines[1:-1]).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}") + 1
        if start >= 0 and end > start:
            return json.loads(text[start:end])
        raise ValueError(f"Could not parse JSON: {text}")


def run_task(difficulty: str) -> float:
    print(f"[STEP] ===== Running {difficulty.upper()} task =====")

    reset_res = requests.post(
        f"{SPACE_URL}/reset",
        json={"task_type": difficulty},
        timeout=60
    )
    print(f"[DEBUG] reset status: {reset_res.status_code}")
    reset_res.raise_for_status()

    reset_data = reset_res.json()
    observation = reset_data.get("observation", reset_data)
    email = observation.get("email", observation)

    sender = email.get("sender", "unknown")
    subject = email.get("subject", "no subject")
    body = email.get("body", "")
    print(f"[STEP] Email: {subject}")

    if difficulty == "easy":
        prompt = (
            f"Classify this email into spam, promotion, or important.\n"
            f"From: {sender}\nSubject: {subject}\nBody: {body}\n\n"
            f'Respond ONLY with JSON: {{"category": "spam"}} or {{"category": "promotion"}} or {{"category": "important"}}'
        )
    else:
        thread = observation.get("thread_context", [])
        context = "\n".join([f"From {m.get('sender','?')}: {m.get('body','')}" for m in thread]) if thread else "No prior context."
        prompt = (
            f"Write a professional email reply.\n"
            f"Thread:\n{context}\n\n"
            f"Latest email — From: {sender}, Subject: {subject}\nBody: {body}\n\n"
            f'Respond ONLY with JSON: {{"response_text": "your reply here"}}'
        )

    print(f"[STEP] Calling LLM...")
    ai_text = call_llm(prompt)
    print(f"[STEP] LLM replied: {ai_text[:120]}")

    action = parse_action(ai_text)
    print(f"[STEP] Action keys: {list(action.keys())}")

    step_res = requests.post(
        f"{SPACE_URL}/step",
        json={"action": action},
        timeout=60
    )
    step_res.raise_for_status()

    reward = float(step_res.json().get("reward", 0.1))
    reward = max(0.01, min(0.99, reward))
    print(f"[STEP] Reward: {reward:.4f}")
    return reward


def main():
    print("[START] Email Management Inference")

    results = {}
    for difficulty in ["easy", "medium", "hard"]:
        try:
            results[difficulty] = run_task(difficulty)
        except Exception as e:
            print(f"[ERROR] {difficulty} failed: {type(e).__name__}: {e}")
            print(traceback.format_exc())
            raise

    avg = sum(results.values()) / len(results)
    print("[STEP] ===== Final Results =====")
    for d, r in results.items():
        print(f"[STEP] {d.capitalize()} task score: {r:.4f}")
    print(f"[STEP] Average score: {avg:.4f}")
    print("[END] Inference complete")


if __name__ == "__main__":
    main()