"""
Master Career Agent.

Coordinates all sub-agents (Resume, Skill Gap, Roadmap, Interview, Project Recommender)
to produce a unified career assessment:
  - Career Health & Hiring Readiness Scores (via scoring_engine.py)
  - A structured timeline action plan
  - AI Advisor high-level strategy (via Groq)
"""

from utils.llm_service import LLMService
from utils.scoring_engine import calculate_health_score, calculate_readiness_score


class MasterAgent:
    """
    Coordinates and synthesizes all individual agent outputs into a unified
    career readiness summary and actionable preparation plan.
    """

    def __init__(self):
        self.llm_service = LLMService()

    # ------------------------------------------------------------------
    # 1. Unified Action Plan Builder (Deterministic)
    # ------------------------------------------------------------------
    def generate_unified_action_plan(
        self,
        ats_score: float,
        missing_skills: list[str],
        projects: list[dict],
        interview_readiness: float
    ) -> dict:
        """
        Creates a structured, deterministic timeline action plan based on the
        candidate's current skill gaps, project progress, and readiness levels.

        Args:
            ats_score: Resume completeness score.
            missing_skills: List of skills the candidate lacks.
            projects: List of recommended projects.
            interview_readiness: Interview readiness score.

        Returns:
            Dict containing action items for 7, 30, 90, and 180+ days.
        """
        immediate = []
        short_term = []
        medium_term = []
        long_term = []

        # ── Immediate Actions (7 Days) ──
        if ats_score < 80:
            immediate.append("Polish resume structure and address completeness guidelines to improve ATS scan accuracy.")
        else:
            immediate.append("Review resume keywords and ensure they are aligned with your target job description.")
            
        immediate.append("Read and review the 'Easy' level questions in the Interview Coach module.")
        
        if missing_skills:
            immediate.append(f"Select the top priority skill gap: '{missing_skills[0]}' and set up a local practice environment.")
        
        # ── Short-Term Goals (30 Days) ──
        if len(missing_skills) > 0:
            skills_to_learn = ", ".join(missing_skills[:3])
            short_term.append(f"Complete focused tutorials or documentation courses for: {skills_to_learn}.")
            
        # Get beginner/intermediate projects
        beg_or_int_projects = [p for p in projects if p.get("difficulty_label") in ["Beginner", "Intermediate"]]
        if beg_or_int_projects:
            short_term.append(f"Develop and publish project: '{beg_or_int_projects[0]['title']}' to your public portfolio.")
        else:
            short_term.append("Develop one intermediate project that implements database or API integrations.")
            
        if interview_readiness < 65:
            short_term.append("Practice 3 simulated mock interview sessions using the 'Medium' difficulty bank.")
        else:
            short_term.append("Conduct a mock session with a peer or write down comprehensive answers to 10 Medium questions.")

        # ── Medium-Term Goals (90 Days) ──
        if len(missing_skills) > 3:
            skills_to_learn_med = ", ".join(missing_skills[3:6])
            medium_term.append(f"Address secondary skill gaps: {skills_to_learn_med}.")
            
        adv_projects = [p for p in projects if p.get("difficulty_label") == "Advanced"]
        if adv_projects:
            medium_term.append(f"Build advanced capstone project: '{adv_projects[0]['title']}' to showcase end-to-end capabilities.")
        else:
            medium_term.append("Construct a multi-module advanced system demonstrating deployment, containerization, or MLOps.")
            
        medium_term.append("Target a readiness score of 80%+ by completing mock sessions on 'Hard' difficulty questions.")
        medium_term.append("Prepare professional profiles on LinkedIn/GitHub and draft cold outreach templates for target hiring managers.")

        # ── Long-Term Goals (6-12 Months) ──
        long_term.append("Apply to active job roles that match your optimized profile target roles.")
        long_term.append("Contribute to open-source repositories or publish technical guides to establish domain authority.")
        long_term.append("Consistently monitor industry trends and adapt your learning roadmap to incorporate emergent tech stacks.")

        return {
            "immediate_7_days": immediate,
            "short_term_30_days": short_term,
            "medium_term_90_days": medium_term,
            "long_term_goals": long_term
        }

    # ------------------------------------------------------------------
    # 2. AI Career Advisor Summarization (Groq via LLMService)
    # ------------------------------------------------------------------
    def generate_career_assessment(
        self,
        role: str,
        ats_score: float,
        gap_score: float,
        missing_skills: list[str],
        matched_skills: list[str],
        interview_readiness: float,
        avg_portfolio_impact: float,
        health: dict,
        readiness: dict
    ) -> dict:
        """
        Queries Groq via LLMService to produce the AI Career Advisor
        high-level feedback summary.

        Args:
            role: Target career role.
            ats_score: Resume completeness score.
            gap_score: Skill gap score.
            missing_skills: List of missing skills.
            matched_skills: List of possessed skills.
            interview_readiness: Interview readiness score.
            avg_portfolio_impact: Average portfolio score.
            health: Computed health score dict.
            readiness: Computed readiness score dict.

        Returns:
            Dict containing summary, strengths, risks, outlook, and next steps.
        """
        prompt = f"""
        You are an elite executive career advisor and talent strategist.
        Analyze this candidate profile for the target role of '{role}':

        Profile Metrics:
        - Career Health Score: {health['score']}/100 ({health['label']})
        - Hiring Readiness Score: {readiness['score']}/100 ({readiness['label']})
        - Resume ATS Score: {ats_score}/100
        - Skill Gap Score: {gap_score}%
        - Possessed Skills: {matched_skills}
        - Missing Skills: {missing_skills}
        - Interview Preparation Readiness: {interview_readiness}%
        - Portfolio Strength: {avg_portfolio_impact}/100

        Provide professional, strategic, and high-level career advisory feedback.
        Be specific to the target role.
        """

        schema = """
        {
            "career_summary": "High-level summary of the candidate's career standing and strategic direction (string)",
            "strengths_assessment": [
                "Major strength 1 with career context",
                "Major strength 2 with career context",
                "Major strength 3 with career context"
            ],
            "risks_assessment": [
                "Critical risk/weakness 1 and how it affects hiring",
                "Critical risk/weakness 2 and how it affects hiring",
                "Critical risk/weakness 3 and how it affects hiring"
            ],
            "hiring_outlook": "Assessment of current market demand for this role and the candidate's competitive advantage (string)",
            "recommended_next_steps": [
                "Strategic next step 1",
                "Strategic next step 2",
                "Strategic next step 3"
            ]
        }
        """

        result = self.llm_service.generate_json(prompt, schema)

        # Safety defaults
        defaults = {
            "career_summary": f"Your preparation puts you in a good position to target {role} roles. Strengthening missing technical skill areas will elevate your profile competitiveness.",
            "strengths_assessment": [f"Possesses core foundation skills: {', '.join(matched_skills[:3]) if matched_skills else 'Standard baseline python skillset'}"],
            "risks_assessment": [f"Missing required technical competencies: {', '.join(missing_skills[:3]) if missing_skills else 'No major gaps'}"],
            "hiring_outlook": "Strong market demand. Opportunities are highly competitive, prioritizing candidates with verified portfolio projects.",
            "recommended_next_steps": ["Complete recommended portfolio projects", "Review scenario interview questions", "Optimize resume keywords"]
        }
        for key, val in defaults.items():
            if key not in result:
                result[key] = val

        return result

    # ------------------------------------------------------------------
    # 3. Main Synthesis Pipeline
    # ------------------------------------------------------------------
    def run_full_orchestration(
        self,
        role: str,
        ats_score: float,
        gap_score: float,
        missing_skills: list[str],
        matched_skills: list[str],
        interview_readiness: float,
        projects: list[dict]
    ) -> dict:
        """
        Executes the entire master career agent pipeline.

        Args:
            role: Target career role.
            ats_score: Resume completeness/ATS score.
            gap_score: Skill gap score.
            missing_skills: List of missing skills.
            matched_skills: List of possessed skills.
            interview_readiness: Interview readiness score.
            projects: List of recommended projects.

        Returns:
            Consolidated dict containing all computed scores, action plans,
            and AI advisory outputs.
        """
        # Calculate average portfolio impact of projects
        if projects:
            avg_portfolio = sum(p.get("portfolio_impact", 0) for p in projects) / len(projects)
        else:
            avg_portfolio = 50.0  # default baseline
        avg_portfolio = round(avg_portfolio, 1)

        # 1. Scoring Engine
        health = calculate_health_score(ats_score, gap_score, interview_readiness, avg_portfolio)
        readiness = calculate_readiness_score(ats_score, gap_score, interview_readiness, avg_portfolio)

        # 2. Unified Action Plan
        action_plan = self.generate_unified_action_plan(
            ats_score=ats_score,
            missing_skills=missing_skills,
            projects=projects,
            interview_readiness=interview_readiness
        )

        # 3. AI Career Assessment
        assessment = self.generate_career_assessment(
            role=role,
            ats_score=ats_score,
            gap_score=gap_score,
            missing_skills=missing_skills,
            matched_skills=matched_skills,
            interview_readiness=interview_readiness,
            avg_portfolio_impact=avg_portfolio,
            health=health,
            readiness=readiness
        )

        return {
            "target_role": role,
            "health_score": health,
            "readiness_score": readiness,
            "action_plan": action_plan,
            "assessment": assessment,
            "subsystem_stats": {
                "ats_score": ats_score,
                "gap_score": gap_score,
                "interview_readiness": interview_readiness,
                "avg_portfolio_impact": avg_portfolio,
                "missing_skills_count": len(missing_skills),
                "recommended_projects_count": len(projects)
            }
        }
