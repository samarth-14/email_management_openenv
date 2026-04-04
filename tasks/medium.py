from models import Email

# Sample emails requiring responses
MEDIUM_EMAILS = [
    Email(
        id="medium_001",
        sender="customer@email.com",
        subject="Product not working",
        body="I bought your product last week and it stopped working today. Very disappointed. What can you do about this?",
        timestamp="2026-04-01 11:00:00"
    ),
    Email(
        id="medium_002",
        sender="partner@business.com",
        subject="Meeting reschedule request",
        body="Hi, can we move our Thursday 2pm meeting to Friday 10am? Let me know if that works for you.",
        timestamp="2026-04-02 10:15:00"
    ),
    Email(
        id="medium_003",
        sender="newclient@corp.com",
        subject="Pricing inquiry",
        body="Hello, I'm interested in your enterprise plan. Could you send me pricing details and a comparison with the standard plan?",
        timestamp="2026-04-03 13:45:00"
    ),
]

def grade_medium_task(email_id: str, response_text: str) -> float:
    """
    Grade the email response quality
    Returns score between 0.0 and 1.0
    """
    if not response_text or len(response_text.strip()) < 10:
        return 0.0
    
    response_lower = response_text.lower()
    score = 0.0
    
    # Check for basic politeness (0.2 points)
    polite_words = ["thank", "please", "sorry", "appreciate", "hello", "hi", "regards"]
    if any(word in response_lower for word in polite_words):
        score += 0.2
    
    # Email-specific checks
    if email_id == "medium_001":  # Product issue
        if "sorry" in response_lower or "apologize" in response_lower:
            score += 0.3
        if "replace" in response_lower or "refund" in response_lower or "fix" in response_lower:
            score += 0.3
        if "contact" in response_lower or "support" in response_lower:
            score += 0.2
            
    elif email_id == "medium_002":  # Meeting reschedule
        if "friday" in response_lower:
            score += 0.4
        if "confirm" in response_lower or "works" in response_lower or "available" in response_lower:
            score += 0.4
            
    elif email_id == "medium_003":  # Pricing inquiry
        if "pricing" in response_lower or "price" in response_lower or "cost" in response_lower:
            score += 0.3
        if "enterprise" in response_lower or "plan" in response_lower:
            score += 0.3
        if "attach" in response_lower or "send" in response_lower or "information" in response_lower:
            score += 0.2
    
    return min(score, 1.0)  # Cap at 1.0