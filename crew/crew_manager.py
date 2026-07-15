"""
CareerCrew Manager.

Instantiates the sequential Crew pipeline on demand, wiring all 6 agents
and tasks via lazy factory functions. Exposes a clean interface for the
Streamlit agentic page.

NOTE: All instantiation is deferred to the first run() call to prevent
module-level LLM initialization and Pydantic v1 errors on Python 3.14.
"""

import logging
from crew.crewai_compat import Crew, HAS_CREWAI

logger = logging.getLogger(__name__)


class CareerCrewManager:
    """
    Manages the CrewAI sequential pipeline.

    When the native CrewAI package is available, delegates to Crew.kickoff().
    When running in fallback mode (Python 3.14), execution is handled by
    CareerCrewWorkflow in workflow.py.
    """

    def __init__(self):
        self.has_native_crewai = HAS_CREWAI
        self._crew = None

    def _build_crew(self) -> Crew:
        """Lazily builds the Crew on first call."""
        if self._crew is None:
            from crew.agents import get_crew_agents
            from crew.tasks import get_crew_tasks
            agents = get_crew_agents()
            tasks = get_crew_tasks(agents)
            self._crew = Crew(
                agents=list(agents.values()),
                tasks=tasks,
                verbose=True
            )
        return self._crew

    def get_agent_labels(self) -> list:
        """
        Returns display labels for each step in the Streamlit UI.

        Returns:
            List of dicts with 'step', 'label', 'role' fields.
        """
        return [
            {"step": 1, "label": "Resume Specialist",  "role": "Resume Evaluation Expert"},
            {"step": 2, "label": "Skill Gap Analyst",  "role": "Career Skills Analyst"},
            {"step": 3, "label": "Roadmap Strategist", "role": "Learning Path Planner"},
            {"step": 4, "label": "Interview Coach",    "role": "Technical Interview Mentor"},
            {"step": 5, "label": "Project Mentor",     "role": "Portfolio Builder"},
            {"step": 6, "label": "Career Advisor",     "role": "Senior Career Consultant"},
        ]
