import random
from typing import Dict, Any, Tuple
from models import Email, Action, State
from tasks.easy import EASY_EMAILS, grade_easy_task
from tasks.medium import MEDIUM_EMAILS, grade_medium_task
from tasks.hard import HARD_EMAIL_THREAD, grade_hard_task


class EmailEnvironment:
    """
    OpenEnv environment for email management
    Implements reset(), step(), and state() methods
    """
    
    def __init__(self):
        self.current_state = None
        self.current_task_type = None
        self.email_thread = []
        
    def reset(self, task_type: str = "easy") -> Dict[str, Any]:
        """Reset environment with a new task"""
        self.current_task_type = task_type
        
        if task_type == "easy":
            email = random.choice(EASY_EMAILS)
            self.current_state = State(
                current_email=email,
                task_type="categorize",
                step_count=0
            )
            
        elif task_type == "medium":
            email = random.choice(MEDIUM_EMAILS)
            self.current_state = State(
                current_email=email,
                task_type="respond",
                step_count=0
            )
            
        elif task_type == "hard":
            self.email_thread = HARD_EMAIL_THREAD.copy()
            email = self.email_thread[-1]
            self.current_state = State(
                current_email=email,
                task_type="thread_respond",
                step_count=0
            )
        
        return self.state()
    
    def step(self, action: Dict[str, Any]) -> Tuple[Dict[str, Any], float, bool]:
        """Execute an action and return new state, reward, and done flag"""
        if self.current_state is None:
            raise ValueError("Environment not initialized. Call reset() first.")
        
        self.current_state.step_count += 1
        reward = 0.0
        done = True
        
        if self.current_task_type == "easy":
            category = action.get("category", "")
            reward = grade_easy_task(
                self.current_state.current_email.id,
                category
            )
            
        elif self.current_task_type == "medium":
            response_text = action.get("response_text", "")
            reward = grade_medium_task(
                self.current_state.current_email.id,
                response_text
            )
            
        elif self.current_task_type == "hard":
            response_text = action.get("response_text", "")
            reward = grade_hard_task(
                self.email_thread,
                response_text
            )
        
        return self.state(), reward, done
    
    def state(self) -> Dict[str, Any]:
        """Return current state as a dictionary"""
        if self.current_state is None:
            return {}
        
        state_dict = {
            "email": {
                "id": self.current_state.current_email.id,
                "sender": self.current_state.current_email.sender,
                "subject": self.current_state.current_email.subject,
                "body": self.current_state.current_email.body,
                "timestamp": self.current_state.current_email.timestamp,
            },
            "task_type": self.current_state.task_type,
            "step_count": self.current_state.step_count,
        }
        
        if self.current_task_type == "hard" and self.email_thread:
            state_dict["thread_context"] = [
                {
                    "sender": email.sender,
                    "subject": email.subject,
                    "body": email.body,
                    "timestamp": email.timestamp,
                }
                for email in self.email_thread[:-1]
            ]
        
        return state_dict