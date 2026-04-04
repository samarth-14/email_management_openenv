from pydantic import BaseModel, Field
from typing import Literal, Optional

class Email(BaseModel):
    """Represents an email in the inbox"""
    id: str
    sender: str
    subject: str
    body: str
    timestamp: str
    category: Optional[str] = None  # Will be filled by agent
    
class Action(BaseModel):
    """Action the agent can take"""
    type: Literal["categorize", "respond", "archive"]
    category: Optional[str] = None  # For categorize action
    response_text: Optional[str] = None  # For respond action

class State(BaseModel):
    """Current state of the environment"""
    current_email: Email
    task_type: str
    step_count: int = 0