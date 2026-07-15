"""
CrewAI Compatibility Fallback Layer.

Provides mock implementations of CrewAI components (Agent, Task, Crew)
to ensure compatibility when running on Python versions (like Python 3.14)
where binary wheels for dependencies (regex, tiktoken) fail to compile.
"""

import sys
import logging

logger = logging.getLogger(__name__)

try:
    from crewai import Agent, Task, Crew
    HAS_CREWAI = True
    logger.info("Using native CrewAI package.")
except ImportError:
    HAS_CREWAI = False
    logger.warning("CrewAI package not found or failed to import. Loading fallback compatibility layer.")

    class Agent:
        """Fallback mock class for crewai.Agent."""
        def __init__(
            self,
            role: str,
            goal: str,
            backstory: str,
            verbose: bool = True,
            llm = None
        ):
            self.role = role
            self.goal = goal
            self.backstory = backstory
            self.verbose = verbose
            self.llm = llm

        def __repr__(self) -> str:
            return f"Agent(role={self.role})"

    class Task:
        """Fallback mock class for crewai.Task."""
        def __init__(
            self,
            description: str,
            expected_output: str,
            agent: Agent,
            context: list = None
        ):
            self.description = description
            self.expected_output = expected_output
            self.agent = agent
            self.context = context or []
            self.output = None

        def __repr__(self) -> str:
            return f"Task(description={self.description[:30]}...)"

    class Crew:
        """Fallback mock class for crewai.Crew."""
        def __init__(
            self,
            agents: list[Agent],
            tasks: list[Task],
            verbose: bool = True
        ):
            self.agents = agents
            self.tasks = tasks
            self.verbose = verbose

        def kickoff(self, inputs: dict = None) -> str:
            """Simulates the sequential kickoff execution of tasks."""
            logger.info("Starting mock Crew kickoff execution...")
            return "Mock Crew Execution Complete"
