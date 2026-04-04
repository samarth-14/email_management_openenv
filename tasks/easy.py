from models import Email

# Sample emails for the easy task
EASY_EMAILS = [
    Email(
        id="easy_001",
        sender="deals@shop.com",
        subject="50% OFF EVERYTHING - Limited Time!",
        body="Buy now and save big! Click here for amazing deals!",
        timestamp="2026-04-01 10:00:00"
    ),
    Email(
        id="easy_002",
        sender="boss@company.com",
        subject="Urgent: Q2 Report Due Tomorrow",
        body="Please submit your Q2 report by EOD tomorrow. This is critical for the board meeting.",
        timestamp="2026-04-02 09:30:00"
    ),
    Email(
        id="easy_003",
        sender="lottery@scam.com",
        subject="You've won $1,000,000!!!",
        body="Claim your prize now! Send us your bank details immediately!",
        timestamp="2026-04-03 14:20:00"
    ),
]

# Correct answers for grading
CORRECT_CATEGORIES = {
    "easy_001": "promotion",
    "easy_002": "important",
    "easy_003": "spam"
}

def grade_easy_task(email_id: str, predicted_category: str) -> float:
    """
    Grade the categorization task
    Returns score between 0.0 and 1.0
    """
    correct_category = CORRECT_CATEGORIES.get(email_id)
    
    if correct_category is None:
        return 0.0
    
    # Exact match gets full score
    if predicted_category == correct_category:
        return 1.0
    
    # Partial credit: important vs promotion (both are not spam)
    if {predicted_category, correct_category} == {"important", "promotion"}:
        return 0.3
    
    # Wrong answer
    return 0.0