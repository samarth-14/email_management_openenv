import os
import json
import requests

# Your deployed Space URL
SPACE_URL = os.getenv("SPACE_URL", "https://samm14-email-management-openenv.hf.space")

def run_task(difficulty: str) -> float:
    """Run a single task and return the reward"""
    print(f"[STEP] ===== Running {difficulty.upper()} task =====")
    
    try:
        # Reset environment
        reset_res = requests.post(
            f"{SPACE_URL}/reset",
            json={"task_type": difficulty},
            timeout=30
        )
        reset_res.raise_for_status()
        state = reset_res.json()["observation"]
        print(f"[STEP] Email subject: {state['email']['subject']}")
        
        # Build action based on difficulty
        if difficulty == "easy":
            action = {"category": "important"}
        else:
            action = {
                "response_text": "Thank you for reaching out. I understand the urgency and will prioritize this matter. I will follow up with a solution shortly."
            }
        
        # Execute step
        step_res = requests.post(
            f"{SPACE_URL}/step",
            json={"action": action},
            timeout=30
        )
        step_res.raise_for_status()
        result = step_res.json()
        reward = result["reward"]
        print(f"[STEP] Reward: {reward:.2f}")
        return reward
        
    except Exception as e:
        print(f"[STEP] Error in {difficulty} task: {e}")
        return 0.01  # Return minimum valid score on error


def main():
    """Main entry point"""
    print("[START] Email Management Environment Inference")
    print("[STEP] Initializing environment")
    
    results = {}
    for difficulty in ["easy", "medium", "hard"]:
        results[difficulty] = run_task(difficulty)
    
    avg = sum(results.values()) / len(results)
    
    print("\n[STEP] ===== Final Results =====")
    for d, r in results.items():
        print(f"[STEP] {d.capitalize()} task score: {r:.2f}")
    print(f"[STEP] Average score: {avg:.2f}")
    print("[END] Inference complete")


if __name__ == "__main__":
    main()