import os
import json
from openai import OpenAI
from environment import EmailEnvironment

# Required environment variables from hackathon
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4")
HF_TOKEN = os.getenv("HF_TOKEN", "")

# Initialize OpenAI client
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN if HF_TOKEN else os.getenv("OPENAI_API_KEY", "dummy-key")
)


def run_agent_on_task(env: EmailEnvironment, task_difficulty: str) -> float:
    """
    Run the agent on a single task
    
    Args:
        env: EmailEnvironment instance
        task_difficulty: "easy", "medium", or "hard"
    
    Returns:
        reward: Score between 0.0 and 1.0
    """
    print(f"[STEP] Starting {task_difficulty} task")
    
    # Reset environment
    state = env.reset(task_type=task_difficulty)
    
    # Create prompt for the agent based on difficulty
    if task_difficulty == "easy":
        prompt = f"""You are an email categorization assistant.

Email Details:
From: {state['email']['sender']}
Subject: {state['email']['subject']}
Body: {state['email']['body']}

Task: Categorize this email as one of: spam, promotion, or important

Respond with ONLY a JSON object in this format:
{{"category": "spam"}}

or

{{"category": "promotion"}}

or

{{"category": "important"}}"""

    elif task_difficulty == "medium":
        prompt = f"""You are an email response assistant.

Email Details:
From: {state['email']['sender']}
Subject: {state['email']['subject']}
Body: {state['email']['body']}

Task: Write a professional response to this email.

Respond with ONLY a JSON object in this format:
{{"response_text": "your response here"}}"""

    else:  # hard
        thread_context = state.get('thread_context', [])
        thread_text = "\n\n".join([
            f"From: {msg['sender']}\nSubject: {msg['subject']}\nBody: {msg['body']}"
            for msg in thread_context
        ])
        
        prompt = f"""You are an email thread management assistant.

Previous conversation:
{thread_text}

Latest email:
From: {state['email']['sender']}
Subject: {state['email']['subject']}
Body: {state['email']['body']}

Task: Write a response that addresses the latest email while considering the full conversation context.

Respond with ONLY a JSON object in this format:
{{"response_text": "your response here"}}"""
    
    print(f"[STEP] Calling AI model for {task_difficulty} task")
# Call AI model
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a helpful email management assistant. Always respond with valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        # Extract response
        ai_response = response.choices[0].message.content.strip()
        print(f"[STEP] AI response received: {ai_response[:100]}...")
        
        # Parse JSON response
        # Remove markdown code blocks if present
        if "```json" in ai_response:
            ai_response = ai_response.split("```json")[1].split("```")[0].strip()
        elif "```" in ai_response:
            ai_response = ai_response.split("```")[1].split("```")[0].strip()
        
        action = json.loads(ai_response)
        
    except Exception as e:
        print(f"[STEP] Error calling AI model: {e}")
        # Fallback action
        if task_difficulty == "easy":
            action = {"category": "important"}
        else:
            action = {"response_text": "Thank you for your email. I will get back to you shortly."}
    
    # Execute action in environment
    print(f"[STEP] Executing action: {action}")
    new_state, reward, done = env.step(action)
    
    print(f"[STEP] Task completed. Reward: {reward:.2f}")
    
    return reward


def main():
    """
    Main inference function - runs all tasks and outputs results
    """
    print("[START] Email Management Environment Inference")
    print("[STEP] Initializing environment")
    
    env = EmailEnvironment()
    
    # Run tasks for each difficulty
    results = {}
    
    for difficulty in ["easy", "medium", "hard"]:
        print(f"\n[STEP] ===== Running {difficulty.upper()} task =====")
        reward = run_agent_on_task(env, difficulty)
        results[difficulty] = reward
    
    # Calculate average score
    avg_score = sum(results.values()) / len(results)
    
    print("\n[STEP] ===== Final Results =====")
    print(f"[STEP] Easy task score: {results['easy']:.2f}")
    print(f"[STEP] Medium task score: {results['medium']:.2f}")
    print(f"[STEP] Hard task score: {results['hard']:.2f}")
    print(f"[STEP] Average score: {avg_score:.2f}")
    
    print("[END] Inference complete")
    
    return results


if __name__ == "__main__":
    main()