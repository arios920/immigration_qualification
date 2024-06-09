# Specify the O1A criteria
O_1A_CRITERIA = [
    "Awards",
    "Membership",
    "Press",
    "Judging",
    "Original contribution",
    "Scholarly articles",
    "Critical employment",
    "High remuneration"
]

def score_achievements(classifications):
    """
    Score the achievements based on the classifications by converting probabilities to scores.
    """
    scores = {criterion: round(classifications[criterion] * 10) for criterion in O_1A_CRITERIA}
    return scores

def generate_rating(scores):
    """
    Generate the final rating based on average scores.
    """
    total_score = sum(scores.values())
    num_criteria = len(scores)
    average_score = total_score / num_criteria if num_criteria > 0 else 0
    
    # Use average here for final score output, and set thresholds for high/medium/low
    if average_score >= 6:
        return "high"
    elif average_score >= 3:
        return "medium"
    else:
        return "low"
