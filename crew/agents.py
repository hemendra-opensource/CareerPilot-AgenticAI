"""
CrewAI Agents Configuration.

Defines the custom LLM wrapper that routes all LLM requests through
LLMService (Groq) and provides factory functions for the 6 CrewAI agents.

IMPORTANT: Agent instances are created lazily via get_crew_agents() to
avoid module-level side effects (LLM init, Pydantic v1 errors on
Python 3.14) during Streamlit's multi-threaded page import phase.
"""

from crew.crewai_compat import Agent, HAS_CREWAI


class LLMServiceWrapper:
    """
    Minimal LLM wrapper that routes CrewAI prompt calls to LLMService.

    Intentionally avoids inheriting from LangChain's SimpleChatModel
    (which depends on Pydantic v1, broken on Python 3.14). CareerPilot
    uses the fallback crewai_compat layer which accepts any object as
    llm= without invoking it directly.
    """

    def __init__(self):
        self._service = None

    def _get_service(self):
        if self._service is None:
            from utils.llm_service import LLMService
            self._service = LLMService()
        return self._service

    def generate(self, prompt: str) -> str:
        """Delegate to centralized LLMService."""
        return self._get_service().generate_text(prompt)

    def __call__(self, prompt: str) -> str:
        return self.generate(prompt)


def get_crew_agents() -> dict:
    """
    Creates and returns the 6 CrewAI agent instances.

    Called lazily only when the agentic workflow page is launched,
    NOT at module import time.

    Returns:
        Dict mapping agent key -> Agent instance.
    """
    llm_model = LLMServiceWrapper()

    resume_specialist = Agent(
        role="Resume Evaluation Expert",
        goal="Extract, structure, and evaluate resume information, checking formatting completeness.",
        backstory=(
            "You are an elite technical recruiter specializing in profile screening. "
            "You analyze candidate resumes to extract structured details, identify format strengths, "
            "and calculate ATS completeness scores."
        ),
        verbose=True,
        llm=llm_model
    )

    skill_gap_analyst = Agent(
        role="Career Skills Analyst",
        goal="Compare current candidate skills against target role databases to identify missing items.",
        backstory=(
            "You are a talent development expert. You analyze technical skill profiles, compare them "
            "against career track requirements, and calculate deterministic gap percentage values."
        ),
        verbose=True,
        llm=llm_model
    )

    roadmap_strategist = Agent(
        role="Learning Path Planner",
        goal="Create a structured, timeline-based learning roadmap to close identified skill gaps.",
        backstory=(
            "You are a technical curriculum manager. You organize skill gaps into progressive study blocks "
            "(Beginner, Intermediate, Advanced) and schedule timeline tracks based on gap severity."
        ),
        verbose=True,
        llm=llm_model
    )

    interview_coach = Agent(
        role="Technical Interview Mentor",
        goal="Generate mock interview sessions, expected outline responses, and readiness score ratings.",
        backstory=(
            "You are a senior technical advisor. You prepare mock question sheets (Technical, HR, Scenario) "
            "and calculate interview readiness grades based on candidate profiles."
        ),
        verbose=True,
        llm=llm_model
    )

    project_mentor = Agent(
        role="Portfolio Builder",
        goal="Recommend target portfolio projects with development roadmaps and impact scores.",
        backstory=(
            "You are an engineering mentor. You select practical capstone and baseline projects "
            "designed to close candidate skill gaps while scoring resume and portfolio value."
        ),
        verbose=True,
        llm=llm_model
    )

    career_advisor = Agent(
        role="Senior Career Consultant",
        goal="Aggregate all diagnostic inputs and compute Career Health and Hiring Readiness grades.",
        backstory=(
            "You are a chief career consultant. You consolidate resume completeness, skill matches, "
            "roadmaps, mock interview scores, and recommended projects into one final executive plan."
        ),
        verbose=True,
        llm=llm_model
    )

    return {
        "resume_specialist": resume_specialist,
        "skill_gap_analyst": skill_gap_analyst,
        "roadmap_strategist": roadmap_strategist,
        "interview_coach": interview_coach,
        "project_mentor": project_mentor,
        "career_advisor": career_advisor,
    }
