"""
CrewAI Task Definitions.

Defines the 6 sequential tasks linked to their respective agents.
Tasks are created lazily via get_crew_tasks() to avoid module-level
agent instantiation during the Streamlit import phase.
"""

from crew.crewai_compat import Task


def get_crew_tasks(agents: dict) -> list:
    """
    Creates and returns the 6 sequential CrewAI task instances.

    Args:
        agents: Dict returned by get_crew_agents(), mapping name -> Agent.

    Returns:
        Ordered list of Task instances for Crew assembly.
    """
    task_analyze_resume = Task(
        description=(
            "Audit the candidate's resume parameters: parse contact blocks, work experience, "
            "and education profiles. Identify formatting strengths, risk areas, and calculate "
            "the resume ATS completeness rating."
        ),
        expected_output=(
            "A structured dictionary containing candidate name, contact blocks, strengths, "
            "weaknesses, and completeness_score."
        ),
        agent=agents["resume_specialist"]
    )

    task_analyze_skill_gaps = Task(
        description=(
            "Compare the candidate's possessed skill set against the target role track requirements "
            "retrieved from the role database. Identify specific missing skills, matched skills, "
            "and compute the final skill gap score."
        ),
        expected_output=(
            "A dictionary containing target_role, gap_score, missing_skills list, "
            "and matched_skills list."
        ),
        agent=agents["skill_gap_analyst"],
        context=[task_analyze_resume]
    )

    task_analyze_roadmap = Task(
        description=(
            "Map out a personalized study curriculum to bridge the candidate's skill gaps. "
            "Divide competencies into Beginner, Intermediate, and Advanced milestones, and assign "
            "a study duration timeframe."
        ),
        expected_output=(
            "A dictionary detailing stages config, monthly study schedules, and priority list."
        ),
        agent=agents["roadmap_strategist"],
        context=[task_analyze_skill_gaps]
    )

    task_analyze_interview = Task(
        description=(
            "Evaluate the candidate's mock interview preparedness. Extract role-relevant questions "
            "and compute the readiness index score by integrating resume completeness and gap metrics."
        ),
        expected_output=(
            "A dictionary containing the readiness score, mock question pools, and critical weakness zones."
        ),
        agent=agents["interview_coach"],
        context=[task_analyze_roadmap]
    )

    task_analyze_projects = Task(
        description=(
            "Generate a curated catalog of portfolio projects designed to close candidate skill gaps. "
            "Score each project's portfolio, resume, and hiring impact value."
        ),
        expected_output=(
            "A list of recommended project dicts with titles, skills learned, and composite priority grades."
        ),
        agent=agents["project_mentor"],
        context=[task_analyze_interview]
    )

    task_analyze_master = Task(
        description=(
            "Consolidate all individual agent outputs. Run the scoring engine to calculate the "
            "unified Career Health and Hiring Readiness grades. Compile the Unified Action Plan "
            "and request final AI career advisory commentaries."
        ),
        expected_output=(
            "A consolidated master dictionary containing Health and Readiness scores, action timelines, "
            "and high-level advisor assessments."
        ),
        agent=agents["career_advisor"],
        context=[task_analyze_projects]
    )

    return [
        task_analyze_resume,
        task_analyze_skill_gaps,
        task_analyze_roadmap,
        task_analyze_interview,
        task_analyze_projects,
        task_analyze_master
    ]
