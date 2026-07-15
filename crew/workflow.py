"""
CareerCrew Workflow Orchestrator.

Implements the sequential multi-agent pipeline by invoking each existing
CareerPilot agent in order, capturing per-step outputs, and aggregating
them into a unified result. Provides robust error handling, status
callbacks for Streamlit live display, and graceful continuation on
partial failures.

Architecture:
    ResumeAnalyzerAgent → SkillGapAgent → RoadmapAgent →
    InterviewAgent → ProjectAgent → MasterAgent
"""

import logging
from typing import Callable, Optional
from agents.resume_agent import ResumeAnalyzerAgent
from agents.skill_gap_agent import SkillGapAgent
from agents.roadmap_agent import RoadmapAgent
from agents.interview_agent import InterviewAgent
from agents.project_agent import ProjectAgent
from agents.master_agent import MasterAgent

logger = logging.getLogger(__name__)


class AgentStepResult:
    """Lightweight dataclass holding the status and output of one agent step."""

    def __init__(self, step: int, label: str, status: str, data: dict, error: str = ""):
        self.step = step
        self.label = label
        self.status = status        # "success" | "failed" | "skipped"
        self.data = data
        self.error = error

    def to_dict(self) -> dict:
        return {
            "step": self.step,
            "label": self.label,
            "status": self.status,
            "data": self.data,
            "error": self.error
        }


class CareerCrewWorkflow:
    """
    Executes the 6-agent career analysis pipeline sequentially.
    Each agent receives outputs from prior agents through shared context.

    Provides an optional status_callback to stream live updates to Streamlit.
    """

    def __init__(self):
        self.resume_agent   = ResumeAnalyzerAgent()
        self.gap_agent      = SkillGapAgent()
        self.roadmap_agent  = RoadmapAgent()
        self.interview_agent = InterviewAgent()
        self.project_agent  = ProjectAgent()
        self.master_agent   = MasterAgent()

    # ------------------------------------------------------------------
    # Sequential pipeline runner
    # ------------------------------------------------------------------
    def run(
        self,
        resume_text: str,
        target_role: str,
        status_callback: Optional[Callable[[int, str, str], None]] = None
    ) -> dict:
        """
        Runs all 6 agents in sequence and aggregates results.

        Args:
            resume_text: Plain text extracted from the candidate's resume.
            target_role: Selected target career track.
            status_callback: Optional callable(step, label, status) for live UI updates.

        Returns:
            Dict containing all step results and the final master orchestration output.
        """
        steps: list[AgentStepResult] = []
        context: dict = {"target_role": target_role, "resume_text": resume_text}

        def _notify(step: int, label: str, status: str):
            logger.info(f"Step {step} [{label}]: {status}")
            if status_callback:
                status_callback(step, label, status)

        # ── Step 1: Resume Agent ──────────────────────────────────────
        _notify(1, "Resume Specialist", "running")
        try:
            # Resume agent expects an uploaded PDF file object; in agentic
            # mode we receive pre-extracted resume text. We synthesize a
            # minimal result from the text without re-parsing the PDF.
            ats_score = self._estimate_ats_from_text(resume_text)
            resume_result = {
                "completeness_score": ats_score,
                "extracted_text": resume_text,
                "personal_details": {"name": "Candidate"},
                "strengths": self._extract_strengths_from_score(ats_score),
                "weaknesses": self._extract_weaknesses_from_score(ats_score),
                "ats_feedback": {}
            }
            context["resume_result"] = resume_result
            steps.append(AgentStepResult(1, "Resume Specialist", "success", resume_result))
            _notify(1, "Resume Specialist", "success")
        except Exception as exc:
            logger.error(f"Resume Agent failed: {exc}")
            resume_result = {"completeness_score": 70.0}
            context["resume_result"] = resume_result
            steps.append(AgentStepResult(1, "Resume Specialist", "failed", {}, str(exc)))
            _notify(1, "Resume Specialist", "failed")

        # ── Step 2: Skill Gap Agent ───────────────────────────────────
        _notify(2, "Skill Gap Analyst", "running")
        try:
            candidate_skills = self._extract_skills_from_text(resume_text)
            gap_result = self.gap_agent.analyze_gaps(candidate_skills, target_role)
            gap_result["target_role"] = target_role
            context["gap_result"] = gap_result
            steps.append(AgentStepResult(2, "Skill Gap Analyst", "success", gap_result))
            _notify(2, "Skill Gap Analyst", "success")
        except Exception as exc:
            logger.error(f"Skill Gap Agent failed: {exc}")
            gap_result = {"gap_score": 50.0, "missing_skills": [], "matched_skills": [], "target_role": target_role}
            context["gap_result"] = gap_result
            steps.append(AgentStepResult(2, "Skill Gap Analyst", "failed", {}, str(exc)))
            _notify(2, "Skill Gap Analyst", "failed")

        # ── Step 3: Roadmap Agent ─────────────────────────────────────
        _notify(3, "Roadmap Strategist", "running")
        try:
            candidate_skills_for_roadmap = context["gap_result"].get("matched_skills", [])
            if not candidate_skills_for_roadmap:
                candidate_skills_for_roadmap = self._extract_skills_from_text(resume_text)
            roadmap_result = self.roadmap_agent.generate_roadmap(
                candidate_skills_for_roadmap,
                target_role,
                context["gap_result"].get("gap_score", 50.0)
            )
            context["roadmap_result"] = roadmap_result
            steps.append(AgentStepResult(3, "Roadmap Strategist", "success", roadmap_result))
            _notify(3, "Roadmap Strategist", "success")
        except Exception as exc:
            logger.error(f"Roadmap Agent failed: {exc}")
            roadmap_result = {"forecast": {"current": 50.0}, "timeline_months": 6, "stages": {}, "monthly_plan": {}}
            context["roadmap_result"] = roadmap_result
            steps.append(AgentStepResult(3, "Roadmap Strategist", "failed", {}, str(exc)))
            _notify(3, "Roadmap Strategist", "failed")

        # ── Step 4: Interview Agent ───────────────────────────────────
        _notify(4, "Interview Coach", "running")
        try:
            completeness_score = context["resume_result"].get("completeness_score", 70.0)
            gap_score_for_int  = context["gap_result"].get("gap_score", 50.0)
            roadmap_current    = context["roadmap_result"].get("forecast", {}).get("current", 50.0)
            # Derive difficulty from gap score deterministically
            if gap_score_for_int >= 60:
                difficulty = "Beginner"
            elif gap_score_for_int >= 30:
                difficulty = "Intermediate"
            else:
                difficulty = "Advanced"
            interview_result  = self.interview_agent.run_full_analysis(
                role=target_role,
                difficulty=difficulty,
                completeness_score=completeness_score,
                gap_score=gap_score_for_int,
                roadmap_current=roadmap_current,
                missing_skills=context["gap_result"].get("missing_skills", []),
                matched_skills=context["gap_result"].get("matched_skills", [])
            )
            context["interview_result"] = interview_result
            steps.append(AgentStepResult(4, "Interview Coach", "success", interview_result))
            _notify(4, "Interview Coach", "success")
        except Exception as exc:
            logger.error(f"Interview Agent failed: {exc}")
            interview_result = {"readiness": {"score": 50.0}, "weak_areas": {}}
            context["interview_result"] = interview_result
            steps.append(AgentStepResult(4, "Interview Coach", "failed", {}, str(exc)))
            _notify(4, "Interview Coach", "failed")

        # ── Step 5: Project Agent ─────────────────────────────────────
        _notify(5, "Project Mentor", "running")
        try:
            readiness_score = context["interview_result"].get("readiness", {}).get("score", 50.0)
            roadmap_current = context["roadmap_result"].get("forecast", {}).get("current", 50.0)
            project_result  = self.project_agent.run_full_analysis(
                role=target_role,
                missing_skills=context["gap_result"].get("missing_skills", []),
                matched_skills=context["gap_result"].get("matched_skills", []),
                gap_score=context["gap_result"].get("gap_score", 50.0),
                readiness_score=readiness_score,
                roadmap_current=roadmap_current
            )
            context["project_result"] = project_result
            steps.append(AgentStepResult(5, "Project Mentor", "success", project_result))
            _notify(5, "Project Mentor", "success")
        except Exception as exc:
            logger.error(f"Project Agent failed: {exc}")
            project_result = {"beginner": [], "intermediate": [], "advanced": [], "stats": {"avg_portfolio_impact": 50.0}}
            context["project_result"] = project_result
            steps.append(AgentStepResult(5, "Project Mentor", "failed", {}, str(exc)))
            _notify(5, "Project Mentor", "failed")

        # ── Step 6: Master Agent ──────────────────────────────────────
        _notify(6, "Career Advisor", "running")
        try:
            all_projects = (
                context["project_result"].get("beginner", []) +
                context["project_result"].get("intermediate", []) +
                context["project_result"].get("advanced", [])
            )
            master_result = self.master_agent.run_full_orchestration(
                role=target_role,
                ats_score=context["resume_result"].get("completeness_score", 70.0),
                gap_score=context["gap_result"].get("gap_score", 50.0),
                missing_skills=context["gap_result"].get("missing_skills", []),
                matched_skills=context["gap_result"].get("matched_skills", []),
                interview_readiness=context["interview_result"].get("readiness", {}).get("score", 50.0),
                projects=all_projects
            )
            context["master_result"] = master_result
            steps.append(AgentStepResult(6, "Career Advisor", "success", master_result))
            _notify(6, "Career Advisor", "success")
        except Exception as exc:
            logger.error(f"Master Agent failed: {exc}")
            master_result = {}
            context["master_result"] = master_result
            steps.append(AgentStepResult(6, "Career Advisor", "failed", {}, str(exc)))
            _notify(6, "Career Advisor", "failed")

        return {
            "steps": [s.to_dict() for s in steps],
            "context": context,
            "success_count": sum(1 for s in steps if s.status == "success"),
            "failed_count": sum(1 for s in steps if s.status == "failed"),
        }

    # ------------------------------------------------------------------
    # Deterministic helper utilities
    # ------------------------------------------------------------------
    def _estimate_ats_from_text(self, text: str) -> float:
        """
        Estimates ATS completeness from resume text length/structure.
        Returns a score between 40.0 and 90.0.
        """
        score = 40.0
        text_lower = text.lower()
        sections = ["experience", "education", "skills", "summary", "contact", "email", "project"]
        for section in sections:
            if section in text_lower:
                score += 7.0
        return round(min(score, 90.0), 1)

    def _extract_strengths_from_score(self, score: float) -> list[str]:
        """Generates strength labels based on the estimated ATS score."""
        if score >= 80:
            return ["Resume formatting is comprehensive", "Key sections are clearly present"]
        elif score >= 60:
            return ["Core professional sections are present"]
        return ["Basic profile structure detected"]

    def _extract_weaknesses_from_score(self, score: float) -> list[str]:
        """Generates weakness labels based on the estimated ATS score."""
        if score < 60:
            return ["Missing quantifiable experience metrics", "Several key sections absent"]
        elif score < 80:
            return ["Consider adding career summary section and measurable outcomes"]
        return ["Profile appears comprehensive"]

    def _extract_skills_from_text(self, text: str) -> list[str]:
        """
        Extracts likely skill tokens from resume text using basic keyword matching
        against the full role database skill vocabulary (deterministic, no LLM).
        """
        from utils.role_database import ROLE_DATABASE
        all_role_skills: set[str] = set()
        for skills in ROLE_DATABASE.values():
            for skill in skills:
                all_role_skills.add(skill)

        text_lower = text.lower()
        found = []
        for skill in all_role_skills:
            if skill.lower() in text_lower:
                found.append(skill)
        return found
