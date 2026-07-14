"""
Scoring Engine for Master Career Agent.

Calculates deterministic scores for:
  - Career Health Score (0-100)
  - Hiring Readiness Score (0-100)

Provides categorizations and labels without calling external APIs.
"""

def get_health_label(score: float) -> str:
    """Returns the descriptive label for Career Health Score."""
    if score >= 90:
        return "Excellent 🟢"
    elif score >= 70:
        return "Good 🟡"
    elif score >= 50:
        return "Average 🟠"
    else:
        return "Needs Improvement 🔴"

def get_readiness_label(score: float) -> str:
    """Returns the descriptive label for Hiring Readiness Score."""
    if score >= 85:
        return "Highly Ready 🟢"
    elif score >= 65:
        return "Moderately Ready 🟡"
    elif score >= 45:
        return "Needs Preparation 🟠"
    else:
        return "Not Ready / Significant prep needed 🔴"

def calculate_health_score(
    ats_score: float,
    gap_score: float,
    interview_readiness: float,
    avg_portfolio_impact: float
) -> dict:
    """
    Calculates the Career Health Score.

    Formula:
        Health Score = (ATS * 0.25) + ((100 - Gap) * 0.25) + (Interview * 0.25) + (Portfolio * 0.25)

    Args:
        ats_score: Resume completeness / ATS score (0-100)
        gap_score: Skill gap score (0-100)
        interview_readiness: Interview readiness score (0-100)
        avg_portfolio_impact: Average portfolio impact score of recommended projects (0-100)

    Returns:
        Dict with score (float), label (str), and breakdown details.
    """
    skill_match = max(0.0, 100.0 - gap_score)
    
    score = round(
        (ats_score * 0.25) +
        (skill_match * 0.25) +
        (interview_readiness * 0.25) +
        (avg_portfolio_impact * 0.25),
        1
    )
    
    return {
        "score": score,
        "label": get_health_label(score),
        "breakdown": {
            "resume_optimization": round(ats_score * 0.25, 1),
            "skill_completeness": round(skill_match * 0.25, 1),
            "interview_preparation": round(interview_readiness * 0.25, 1),
            "portfolio_strength": round(avg_portfolio_impact * 0.25, 1)
        }
    }

def calculate_readiness_score(
    ats_score: float,
    gap_score: float,
    interview_readiness: float,
    avg_portfolio_impact: float
) -> dict:
    """
    Calculates the Hiring Readiness Score.

    Formula:
        Readiness Score = (ATS * 0.20) + ((100 - Gap) * 0.30) + (Interview * 0.30) + (Portfolio * 0.20)

    Args:
        ats_score: Resume completeness / ATS score (0-100)
        gap_score: Skill gap score (0-100)
        interview_readiness: Interview readiness score (0-100)
        avg_portfolio_impact: Average portfolio impact score of recommended projects (0-100)

    Returns:
        Dict with score (float), label (str), and breakdown details.
    """
    skill_match = max(0.0, 100.0 - gap_score)
    
    score = round(
        (ats_score * 0.20) +
        (skill_match * 0.30) +
        (interview_readiness * 0.30) +
        (avg_portfolio_impact * 0.20),
        1
    )
    
    return {
        "score": score,
        "label": get_readiness_label(score),
        "breakdown": {
            "resume_quality": round(ats_score * 0.20, 1),
            "skill_match": round(skill_match * 0.30, 1),
            "interview_readiness": round(interview_readiness * 0.30, 1),
            "portfolio_strength": round(avg_portfolio_impact * 0.20, 1)
        }
    }
