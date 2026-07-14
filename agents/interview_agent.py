import random
from utils.llm_service import LLMService
from utils.interview_templates import INTERVIEW_TEMPLATES

class InterviewAgent:
    """
    Orchestrates the Interview Coach pipeline:
    - Filters static questions by role and difficulty
    - Builds 10-question mock interviews
    - Calculates interview readiness score deterministically
    - Detects weak areas from Phase 3 missing skills
    - Generates AI coaching summary via LLMService
    """

    def __init__(self):
        self.llm_service = LLMService()

    # ------------------------------------------------------------------
    # 1. Question Retrieval
    # ------------------------------------------------------------------
    def get_technical_questions(self, role: str, difficulty: str) -> list[dict]:
        """
        Returns technical questions filtered by role and difficulty.

        Args:
            role: Target career role (e.g. 'Data Scientist').
            difficulty: 'Easy', 'Medium', or 'Hard'.

        Returns:
            List of question dicts with question, answer_outline, key_points.
        """
        tech_bank = INTERVIEW_TEMPLATES.get("Technical", {})
        role_bank = tech_bank.get(role, {})
        return role_bank.get(difficulty, [])

    def get_hr_questions(self, difficulty: str) -> list[dict]:
        """
        Returns HR questions filtered by difficulty.

        Args:
            difficulty: 'Easy', 'Medium', or 'Hard'.

        Returns:
            List of question dicts.
        """
        return INTERVIEW_TEMPLATES.get("HR", {}).get(difficulty, [])

    def get_scenario_questions(self, difficulty: str) -> list[dict]:
        """
        Returns scenario-based questions filtered by difficulty.

        Args:
            difficulty: 'Easy', 'Medium', or 'Hard'.

        Returns:
            List of question dicts.
        """
        return INTERVIEW_TEMPLATES.get("Scenario", {}).get(difficulty, [])

    # ------------------------------------------------------------------
    # 2. Mock Interview Builder
    # ------------------------------------------------------------------
    def generate_mock_interview(self, role: str, total: int = 10) -> list[dict]:
        """
        Generates a mock interview of `total` questions sampled across
        Technical (role-specific), HR, and Scenario categories and all
        three difficulty levels.

        Args:
            role: Target career role string.
            total: Total number of questions (default 10).

        Returns:
            Numbered list of question dicts including category and difficulty fields.
        """
        pool: list[dict] = []

        for difficulty in ["Easy", "Medium", "Hard"]:
            for q in self.get_technical_questions(role, difficulty):
                pool.append({**q, "category": "Technical", "difficulty": difficulty})
            for q in self.get_hr_questions(difficulty):
                pool.append({**q, "category": "HR", "difficulty": difficulty})
            for q in self.get_scenario_questions(difficulty):
                pool.append({**q, "category": "Scenario", "difficulty": difficulty})

        # Sample `total` or as many as available
        sample_size = min(total, len(pool))
        selected = random.sample(pool, sample_size)

        # Add question numbers
        return [{"number": i + 1, **q} for i, q in enumerate(selected)]

    # ------------------------------------------------------------------
    # 3. Readiness Score (Fully Deterministic)
    # ------------------------------------------------------------------
    def calculate_readiness_score(
        self,
        completeness_score: float,
        gap_score: float,
        roadmap_current: float
    ) -> dict:
        """
        Calculates the interview readiness score from prior phase data.

        Formula:
            readiness = (completeness × 0.40) + ((100 - gap_score) × 0.40) + (roadmap × 0.20)

        Args:
            completeness_score: Resume completeness score (0-100) from Phase 2.
            gap_score: Skill gap score (0-100) from Phase 3.
            roadmap_current: Current roadmap readiness (0-100) from Phase 4.

        Returns:
            Dict with score, label, and component breakdown.
        """
        skill_match = max(0.0, 100.0 - gap_score)
        score = round(
            (completeness_score * 0.40) +
            (skill_match * 0.40) +
            (roadmap_current * 0.20),
            1
        )

        if score >= 80:
            label = "🟢 Highly Ready"
        elif score >= 60:
            label = "🟡 Moderately Ready"
        elif score >= 40:
            label = "🟠 Needs Preparation"
        else:
            label = "🔴 Significant Preparation Required"

        return {
            "score": score,
            "label": label,
            "breakdown": {
                "resume_completeness": round(completeness_score * 0.40, 1),
                "skill_match": round(skill_match * 0.40, 1),
                "roadmap_coverage": round(roadmap_current * 0.20, 1)
            }
        }

    # ------------------------------------------------------------------
    # 4. Weak Area Detection (Deterministic)
    # ------------------------------------------------------------------
    def detect_weak_areas(self, missing_skills: list[str], role: str) -> dict:
        """
        Flags technical weaknesses using Phase 3 missing skills.

        Args:
            missing_skills: List of skills missing for the target role.
            role: Target career role string.

        Returns:
            Dict with technical_weaknesses, missing_concepts, interview_risk_areas.
        """
        # Technical weaknesses = directly missing required skills
        technical_weaknesses = missing_skills

        # Missing concepts = skills that often appear in interview questions
        tech_bank = INTERVIEW_TEMPLATES.get("Technical", {}).get(role, {})
        all_role_questions = []
        for qs in tech_bank.values():
            all_role_questions.extend(qs)

        missing_lower = {s.lower() for s in missing_skills}
        interview_risk_areas = [
            q["question"]
            for q in all_role_questions
            if any(skill in q["question"].lower() for skill in missing_lower)
        ]

        return {
            "technical_weaknesses": technical_weaknesses,
            "missing_concepts": missing_skills,
            "interview_risk_areas": interview_risk_areas[:5]  # Top 5 risk questions
        }

    # ------------------------------------------------------------------
    # 5. AI Coaching Summary
    # ------------------------------------------------------------------
    def generate_coaching_summary(
        self,
        role: str,
        readiness: dict,
        missing_skills: list[str],
        matched_skills: list[str],
        weak_areas: dict
    ) -> dict:
        """
        Generates an AI coaching narrative using Groq via LLMService.

        Args:
            role: Target career role.
            readiness: Readiness score dict.
            missing_skills: Skills not yet acquired.
            matched_skills: Skills already possessed.
            weak_areas: Weak area detection output.

        Returns:
            Dict with summary, focus areas, common mistakes, and recommendations.
        """
        prompt = f"""
        You are an elite technical interview coach with 15+ years of experience at top tech companies.
        Provide structured, actionable interview preparation advice for a candidate targeting the role of '{role}'.

        Candidate Profile:
        - Interview Readiness Score: {readiness['score']}/100 ({readiness['label']})
        - Possessed Skills: {matched_skills}
        - Missing Skills: {missing_skills}
        - Top Interview Risk Areas: {weak_areas.get('interview_risk_areas', [])}
        - Score Breakdown: Resume={readiness['breakdown']['resume_completeness']}, 
          Skill Match={readiness['breakdown']['skill_match']}, 
          Roadmap={readiness['breakdown']['roadmap_coverage']}

        Provide practical, encouraging, and specific coaching advice.
        """

        schema = """
        {
            "preparation_summary": "Overall assessment of candidate's interview readiness and strategy (string)",
            "key_focus_areas": [
                "Focus area 1 with specific action",
                "Focus area 2 with specific action",
                "Focus area 3 with specific action",
                "Focus area 4 with specific action",
                "Focus area 5 with specific action"
            ],
            "common_mistakes": [
                "Common mistake 1 to avoid",
                "Common mistake 2 to avoid",
                "Common mistake 3 to avoid"
            ],
            "final_recommendations": [
                "Final recommendation 1",
                "Final recommendation 2",
                "Final recommendation 3"
            ]
        }
        """

        coaching = self.llm_service.generate_json(prompt, schema)

        # Safety defaults
        defaults = {
            "preparation_summary": f"Focus on strengthening your knowledge of: {', '.join(missing_skills[:3])} to become more competitive for {role} interviews.",
            "key_focus_areas": [f"Study {skill}" for skill in missing_skills[:5]],
            "common_mistakes": ["Skipping fundamentals", "Not practicing coding problems", "Neglecting behavioral questions"],
            "final_recommendations": ["Build projects using missing skills", "Practice mock interviews weekly", "Review system design concepts"]
        }
        for key, val in defaults.items():
            if key not in coaching:
                coaching[key] = val

        return coaching

    # ------------------------------------------------------------------
    # 6. Full Analysis Pipeline
    # ------------------------------------------------------------------
    def run_full_analysis(
        self,
        role: str,
        difficulty: str,
        completeness_score: float,
        gap_score: float,
        roadmap_current: float,
        missing_skills: list[str],
        matched_skills: list[str]
    ) -> dict:
        """
        Runs the complete interview coaching pipeline and returns all results.

        Args:
            role: Target career role.
            difficulty: Preferred difficulty level.
            completeness_score: From Phase 2 resume analysis.
            gap_score: From Phase 3 skill gap analysis.
            roadmap_current: From Phase 4 readiness forecast.
            missing_skills: From Phase 3 skill gap analysis.
            matched_skills: From Phase 3 skill gap analysis.

        Returns:
            Complete interview coaching result dictionary.
        """
        technical_questions = self.get_technical_questions(role, difficulty)
        hr_questions = self.get_hr_questions(difficulty)
        scenario_questions = self.get_scenario_questions(difficulty)
        mock_interview = self.generate_mock_interview(role)
        readiness = self.calculate_readiness_score(completeness_score, gap_score, roadmap_current)
        weak_areas = self.detect_weak_areas(missing_skills, role)
        coaching = self.generate_coaching_summary(
            role=role,
            readiness=readiness,
            missing_skills=missing_skills,
            matched_skills=matched_skills,
            weak_areas=weak_areas
        )

        return {
            "role": role,
            "difficulty": difficulty,
            "technical_questions": technical_questions,
            "hr_questions": hr_questions,
            "scenario_questions": scenario_questions,
            "mock_interview": mock_interview,
            "readiness": readiness,
            "weak_areas": weak_areas,
            "coaching": coaching
        }
