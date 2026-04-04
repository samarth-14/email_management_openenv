from models import Email
from typing import List

# Email thread (conversation)
HARD_EMAIL_THREAD = [
    Email(
        id="hard_001_msg1",
        sender="client@company.com",
        subject="Project timeline question",
        body="Hi, when can we expect the first draft of the marketing materials?",
        timestamp="2026-04-01 09:00:00"
    ),
    Email(
        id="hard_001_msg2",
        sender="you@yourcompany.com",
        subject="Re: Project timeline question",
        body="We'll have the first draft ready by April 15th.",
        timestamp="2026-04-01 10:30:00"
    ),
    Email(
        id="hard_001_msg3",
        sender="client@company.com",
        subject="Re: Project timeline question",
        body="That's later than expected. Can you expedite? We have a launch on April 20th.",
        timestamp="2026-04-02 08:15:00"
    ),
]

def grade_hard_task(email_thread: List[Email], response_text: str) -> float:
    """
    Grade the context-aware email thread response
    Returns score between 0.0 and 1.0
    """
    if not response_text or len(response_text.strip()) < 15:
        return 0.0
    
    response_lower = response_text.lower()
    score = 0.0
    
    # Basic politeness (0.15 points)
    polite_words = ["thank", "understand", "apologize", "appreciate"]
    if any(word in response_lower for word in polite_words):
        score += 0.15
    
    # References the timeline/dates (0.25 points)
    timeline_refs = ["april 15", "15th", "april 20", "20th", "timeline", "deadline", "launch"]
    if any(ref in response_lower for ref in timeline_refs):
        score += 0.25
    
    # Acknowledges the urgency (0.25 points)
    urgency_words = ["expedite", "rush", "priority", "urgent", "sooner", "faster", "earlier"]
    if any(word in response_lower for word in urgency_words):
        score += 0.25
    
    # Proposes a solution (0.35 points)
    solution_words = ["can", "will", "able to", "move", "adjust", "reschedule", "team", "resources"]
    if any(word in response_lower for word in solution_words):
        score += 0.35
    
    return min(score, 1.0)  # Cap at 1.0