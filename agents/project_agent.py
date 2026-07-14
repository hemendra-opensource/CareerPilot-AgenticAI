"""
Project Recommender Agent.

Orchestrates the full project recommendation pipeline:
  1. Loads static project banks from project_templates.py
  2. Filters projects by role and difficulty
  3. Calculates composite priority scores using 4 weighted factors:
       - Missing Skills Overlap (40%): how many gap skills this project teaches
       - Difficulty Alignment   (30%): whether difficulty matches current readiness
       - Readiness Score        (20%): current interview readiness from Phase 5
       - Roadmap Progress       (10%): how far along the roadmap the candidate is
  4. Compiles career impact analysis per project
  5. Generates AI-personalized coaching summary via LLMService
"""

from utils.llm_service import LLMService
from utils.project_templates import PROJECT_TEMPLATES


class ProjectAgent:
    """
    Agent that recommends practical portfolio projects based on the
    candidate's role, skill gaps, and career roadmap data.
    """

    def __init__(self):
        self.llm_service = LLMService()

    # ------------------------------------------------------------------
    # 1. Project Retrieval
    # ------------------------------------------------------------------
    def get_projects_by_difficulty(
        self,
        role: str,
        difficulty: str
    ) -> list[dict]:
        """
        Returns all projects for a given role and difficulty level.

        Args:
            role: Target career role string.
            difficulty: 'Beginner', 'Intermediate', or 'Advanced'.

        Returns:
            List of project dicts from the static template bank.
        """
        role_bank = PROJECT_TEMPLATES.get(role, {})
        return role_bank.get(difficulty, [])

    def get_all_projects_for_role(self, role: str) -> dict[str, list[dict]]:
        """
        Returns all projects grouped by difficulty for a given role.

        Args:
            role: Target career role string.

        Returns:
            Dict with keys 'Beginner', 'Intermediate', 'Advanced'.
        """
        return PROJECT_TEMPLATES.get(role, {})

    # ------------------------------------------------------------------
    # 2. Composite Priority Scoring (Deterministic, 4-Factor)
    # ------------------------------------------------------------------
    # Difficulty alignment table:
    #   readiness < 40  → Beginner=1.0, Intermediate=0.6, Advanced=0.3
    #   40 ≤ r < 70     → Beginner=0.7, Intermediate=1.0, Advanced=0.6
    #   readiness ≥ 70  → Beginner=0.4, Intermediate=0.8, Advanced=1.0
    _DIFFICULTY_ALIGNMENT: dict[str, dict[str, float]] = {
        "low":    {"Beginner": 1.0, "Intermediate": 0.6, "Advanced": 0.3},
        "medium": {"Beginner": 0.7, "Intermediate": 1.0, "Advanced": 0.6},
        "high":   {"Beginner": 0.4, "Intermediate": 0.8, "Advanced": 1.0},
    }

    def _readiness_tier(self, readiness_score: float) -> str:
        """Maps readiness score to alignment tier key."""
        if readiness_score < 40:
            return "low"
        elif readiness_score < 70:
            return "medium"
        return "high"

    def calculate_gap_priority(
        self,
        project: dict,
        missing_skills: list[str]
    ) -> int:
        """
        Raw count of how many missing skills this project directly teaches.
        Used as a standalone signal and as part of the composite score.

        Args:
            project: Single project dict from the template bank.
            missing_skills: List of skills missing from Phase 3 analysis.

        Returns:
            Integer overlap count (0 = no gap-closing value).
        """
        missing_lower = {s.lower() for s in missing_skills}
        learned_lower = {s.lower() for s in project.get("skills_learned", [])}
        return len(missing_lower & learned_lower)

    def calculate_composite_priority(
        self,
        project: dict,
        difficulty: str,
        missing_skills: list[str],
        readiness_score: float,
        roadmap_current: float
    ) -> float:
        """
        Calculates a 0-100 composite priority score using 4 weighted factors.

        Formula:
            composite = (gap_overlap  × 0.40)
                      + (diff_align   × 0.30)
                      + (readiness    × 0.20)
                      + (roadmap      × 0.10)

        Factor details:
            gap_overlap  : normalised fraction of missing skills this project covers
                           = overlap_count / max(len(skills_learned), 1), scaled ×100
            diff_align   : how well the project difficulty suits current readiness
                           (lookup from _DIFFICULTY_ALIGNMENT table), scaled ×100
            readiness    : candidate's current interview readiness score (0-100)
            roadmap      : candidate's roadmap progress (0-100)

        Args:
            project: Single project dict from the template bank.
            difficulty: 'Beginner', 'Intermediate', or 'Advanced'.
            missing_skills: Skills missing from Phase 3 analysis.
            readiness_score: Interview readiness (0-100) from Phase 5 / Phase 3.
            roadmap_current: Roadmap forecast current progress (0-100) from Phase 4.

        Returns:
            Composite priority score (0.0 – 100.0).
        """
        # Factor 1 – Missing Skills Overlap (40%)
        learned = project.get("skills_learned", [])
        overlap = self.calculate_gap_priority(project, missing_skills)
        max_possible = max(len(learned), 1)
        gap_overlap_norm = min(overlap / max_possible, 1.0) * 100  # 0-100

        # Factor 2 – Difficulty Alignment (30%)
        tier = self._readiness_tier(readiness_score)
        diff_align_norm = self._DIFFICULTY_ALIGNMENT[tier].get(difficulty, 0.5) * 100  # 0-100

        # Factor 3 – Readiness Score (20%) — already 0-100
        readiness_norm = max(0.0, min(readiness_score, 100.0))

        # Factor 4 – Roadmap Progress (10%) — already 0-100
        roadmap_norm = max(0.0, min(roadmap_current, 100.0))

        composite = (
            gap_overlap_norm  * 0.40
            + diff_align_norm * 0.30
            + readiness_norm  * 0.20
            + roadmap_norm    * 0.10
        )
        return round(composite, 2)

    def sort_by_composite_priority(
        self,
        projects: list[dict],
        difficulty: str,
        missing_skills: list[str],
        readiness_score: float,
        roadmap_current: float
    ) -> list[dict]:
        """
        Enriches each project with all priority signals and sorts by
        composite_priority descending so the most relevant projects appear first.

        Priority order respects:
          1. Missing Skills coverage
          2. Career Goal / difficulty alignment with readiness
          3. Current Readiness Score
          4. Roadmap Progress

        Args:
            projects: List of project dicts for one difficulty tier.
            difficulty: Tier label ('Beginner', 'Intermediate', 'Advanced').
            missing_skills: From Phase 3 skill gap analysis.
            readiness_score: From Phase 5 interview readiness (0-100).
            roadmap_current: From Phase 4 roadmap forecast (0-100).

        Returns:
            Sorted list of projects with enrichment fields added.
        """
        enriched = []
        for p in projects:
            gap_count = self.calculate_gap_priority(p, missing_skills)
            composite = self.calculate_composite_priority(
                p, difficulty, missing_skills, readiness_score, roadmap_current
            )
            enriched.append({
                **p,
                "gap_priority":       gap_count,
                "is_gap_closer":      gap_count > 0,
                "difficulty_label":   difficulty,
                "composite_priority": composite,
            })
        return sorted(enriched, key=lambda x: x["composite_priority"], reverse=True)

    # ------------------------------------------------------------------
    # 3. Career Impact Compiler (Deterministic)
    # ------------------------------------------------------------------
    def compile_career_impact(self, project: dict) -> dict:
        """
        Compiles career impact metadata for a single project.

        Args:
            project: Single enriched project dict.

        Returns:
            Dict with portfolio_impact, resume_impact, hiring_value,
            companies_that_value, and gap_priority.
        """
        return {
            "title": project.get("title"),
            "portfolio_impact": project.get("portfolio_impact", 0),
            "resume_impact": project.get("resume_impact", 0),
            "hiring_value": project.get("hiring_value", 0),
            "gap_priority": project.get("gap_priority", 0),
            "companies_that_value": project.get("companies_that_value", []),
            "skills_learned": project.get("skills_learned", []),
            "duration": project.get("duration", "TBD"),
            "is_gap_closer": project.get("is_gap_closer", False)
        }

    # ------------------------------------------------------------------
    # 4. AI Personalization (Groq via LLMService)
    # ------------------------------------------------------------------
    def generate_personalized_recommendations(
        self,
        role: str,
        missing_skills: list[str],
        matched_skills: list[str],
        gap_score: float,
        top_projects: list[dict]
    ) -> dict:
        """
        Uses Groq via LLMService to generate a personalized project
        sequencing strategy and career coaching summary.

        Args:
            role: Target career role.
            missing_skills: Skills not yet acquired.
            matched_skills: Skills already possessed.
            gap_score: Skill gap percentage from Phase 3.
            top_projects: Top priority projects (gap-sorted, all difficulties).

        Returns:
            Dict with overall_strategy, recommended_sequence,
            quick_wins, long_term_goals, and motivational_note.
        """
        top_titles = [p.get("title", "") for p in top_projects[:6]]

        prompt = f"""
        You are a senior career coach specializing in building developer portfolios.
        Provide a personalized project roadmap for a candidate targeting the role of '{role}'.

        Candidate Profile:
        - Target Role: {role}
        - Skill Gap Score: {gap_score}%
        - Possessed Skills: {matched_skills}
        - Missing Skills: {missing_skills}
        - Top Priority Projects (by gap-closing value): {top_titles}

        Create a practical, motivating, and specific project sequencing strategy.
        Focus on building momentum from beginner to advanced projects.
        """

        schema = """
        {
            "overall_strategy": "2-3 sentences describing the overall project-building strategy for this candidate",
            "recommended_sequence": [
                "Step 1: Project title and reason",
                "Step 2: Project title and reason",
                "Step 3: Project title and reason",
                "Step 4: Project title and reason"
            ],
            "quick_wins": [
                "Quick win project 1 with reason",
                "Quick win project 2 with reason"
            ],
            "long_term_goals": [
                "Advanced project goal 1",
                "Advanced project goal 2"
            ],
            "motivational_note": "A short, genuine, encouraging note for the candidate"
        }
        """

        result = self.llm_service.generate_json(prompt, schema)

        # Safety defaults
        defaults = {
            "overall_strategy": f"Build a progressive portfolio starting with beginner projects to gain confidence, then tackle intermediate and advanced projects that directly address your {len(missing_skills)} missing skills.",
            "recommended_sequence": [f"Start with: {t}" for t in top_titles[:4]],
            "quick_wins": [f"Complete {t} for quick portfolio boost" for t in top_titles[:2]],
            "long_term_goals": [f"Master {s} through a project" for s in missing_skills[:2]],
            "motivational_note": "Every expert was once a beginner. Start with one project today and build from there!"
        }
        for key, val in defaults.items():
            if key not in result:
                result[key] = val

        return result

    # ------------------------------------------------------------------
    # 5. Full Pipeline
    # ------------------------------------------------------------------
    def run_full_analysis(
        self,
        role: str,
        missing_skills: list[str],
        matched_skills: list[str],
        gap_score: float,
        readiness_score: float = 50.0,
        roadmap_current: float = 50.0
    ) -> dict:
        """
        Runs the complete project recommendation pipeline.

        Projects are ordered by the 4-factor composite priority score:
          1. Missing Skills coverage (40%)
          2. Difficulty alignment with current readiness (30%)
          3. Interview readiness score (20%)
          4. Roadmap progress (10%)

        Args:
            role: Target career role.
            missing_skills: From Phase 3 skill gap analysis.
            matched_skills: From Phase 3 skill gap analysis.
            gap_score: Skill gap percentage from Phase 3.
            readiness_score: Interview readiness 0-100 from Phase 5 (default 50).
            roadmap_current: Roadmap forecast current progress 0-100 from Phase 4 (default 50).

        Returns:
            Complete recommendation result dict with all difficulty tiers sorted
            by composite priority, career impact analysis, and AI coaching.
        """
        all_projects = self.get_all_projects_for_role(role)

        beginner = self.sort_by_composite_priority(
            all_projects.get("Beginner", []),
            difficulty="Beginner",
            missing_skills=missing_skills,
            readiness_score=readiness_score,
            roadmap_current=roadmap_current
        )
        intermediate = self.sort_by_composite_priority(
            all_projects.get("Intermediate", []),
            difficulty="Intermediate",
            missing_skills=missing_skills,
            readiness_score=readiness_score,
            roadmap_current=roadmap_current
        )
        advanced = self.sort_by_composite_priority(
            all_projects.get("Advanced", []),
            difficulty="Advanced",
            missing_skills=missing_skills,
            readiness_score=readiness_score,
            roadmap_current=roadmap_current
        )

        # Compile career impact for all projects
        all_enriched = beginner + intermediate + advanced
        career_impact = [self.compile_career_impact(p) for p in all_enriched]

        # Top projects for AI personalization — ordered by composite score across all tiers
        top_projects = sorted(
            all_enriched, key=lambda x: x["composite_priority"], reverse=True
        )

        coaching = self.generate_personalized_recommendations(
            role=role,
            missing_skills=missing_skills,
            matched_skills=matched_skills,
            gap_score=gap_score,
            top_projects=top_projects
        )

        return {
            "role": role,
            "beginner": beginner,
            "intermediate": intermediate,
            "advanced": advanced,
            "career_impact": career_impact,
            "coaching": coaching,
            "stats": {
                "total_projects": len(all_enriched),
                "gap_closers": sum(1 for p in all_enriched if p.get("is_gap_closer")),
                "avg_portfolio_impact": round(
                    sum(p.get("portfolio_impact", 0) for p in all_enriched)
                    / max(len(all_enriched), 1), 1
                ),
                "readiness_score": readiness_score,
                "roadmap_current": roadmap_current
            }
        }
