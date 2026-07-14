from utils.llm_service import LLMService
from utils.roadmap_templates import ROADMAP_TEMPLATES
from agents.skill_gap_agent import SkillMatcher

class RoadmapAgent:
    """Orchestrates career roadmap generation based on skill gaps and target roles."""
    
    def __init__(self):
        self.llm_service = LLMService()
        
    def generate_roadmap(self, candidate_skills: list[str], target_role: str, gap_score: float) -> dict:
        """
        Generates a structured career learning roadmap with deterministic schedules and AI advice.
        
        Args:
            candidate_skills: List of skills currently possessed by the candidate.
            target_role: The selected target job role.
            gap_score: The calculated skill gap score (0-100).
            
        Returns:
            A dictionary containing stages, timeline, monthly plan, priority matrix,
            resource repository, career forecast, and AI recommendations.
        """
        if target_role not in ROADMAP_TEMPLATES:
            raise ValueError(f"Target role '{target_role}' not found in roadmap templates database.")
            
        template = ROADMAP_TEMPLATES[target_role]
        stages_config = template["stages"]
        resources_config = template["resources"]
        
        # 1. Map skills to stages case-insensitively
        cand_lower = {s.lower().strip() for s in candidate_skills}
        
        stages_data = {
            "Beginner": [],
            "Intermediate": [],
            "Advanced": []
        }
        
        missing_required = []
        matched_required = []
        
        for stage, skills in stages_config.items():
            for skill in skills:
                skill_lower = skill.lower().strip()
                status = "Matched" if skill_lower in cand_lower else "Missing"
                stages_data[stage].append({
                    "skill": skill,
                    "status": status
                })
                if status == "Matched":
                    matched_required.append(skill)
                else:
                    missing_required.append(skill)
                    
        # Additional elective skills
        all_template_skills_lower = {s.lower().strip() for skills in stages_config.values() for s in skills}
        additional_skills = [s for s in candidate_skills if s.lower().strip() not in all_template_skills_lower]

        # 2. Determine Timeline Track based on Gap Score
        if gap_score <= 25.0:
            timeline_months = 3
        elif gap_score <= 60.0:
            timeline_months = 6
        else:
            timeline_months = 12
            
        # 3. Formulate Month-by-Month Plan
        monthly_plan = {}
        
        # Helper to distribute missing skills from stages into month blocks
        beg_missing = [s["skill"] for s in stages_data["Beginner"] if s["status"] == "Missing"]
        int_missing = [s["skill"] for s in stages_data["Intermediate"] if s["status"] == "Missing"]
        adv_missing = [s["skill"] for s in stages_data["Advanced"] if s["status"] == "Missing"]
        
        if timeline_months == 3:
            monthly_plan["Month 1"] = {
                "focus": "Beginner Core Foundations",
                "skills": beg_missing if beg_missing else ["No gaps! Review: " + ", ".join(stages_config["Beginner"])]
            }
            monthly_plan["Month 2"] = {
                "focus": "Intermediate Frameworks & Methods",
                "skills": int_missing if int_missing else ["No gaps! Reinforce: " + ", ".join(stages_config["Intermediate"])]
            }
            monthly_plan["Month 3"] = {
                "focus": "Advanced Systems & Implementations",
                "skills": adv_missing if adv_missing else ["No gaps! Master: " + ", ".join(stages_config["Advanced"])]
            }
        elif timeline_months == 6:
            monthly_plan["Months 1-2"] = {
                "focus": "Beginner Core Foundations",
                "skills": beg_missing if beg_missing else ["No gaps! Review: " + ", ".join(stages_config["Beginner"])]
            }
            monthly_plan["Months 3-4"] = {
                "focus": "Intermediate Frameworks & Methods",
                "skills": int_missing if int_missing else ["No gaps! Reinforce: " + ", ".join(stages_config["Intermediate"])]
            }
            monthly_plan["Months 5-6"] = {
                "focus": "Advanced Systems & Implementations",
                "skills": adv_missing if adv_missing else ["No gaps! Master: " + ", ".join(stages_config["Advanced"])]
            }
        else:  # 12 Months
            monthly_plan["Months 1-3"] = {
                "focus": "Beginner Core Foundations",
                "skills": beg_missing if beg_missing else ["No gaps! Review: " + ", ".join(stages_config["Beginner"])]
            }
            monthly_plan["Months 4-7"] = {
                "focus": "Intermediate Frameworks & Methods",
                "skills": int_missing if int_missing else ["No gaps! Reinforce: " + ", ".join(stages_config["Intermediate"])]
            }
            monthly_plan["Months 8-12"] = {
                "focus": "Advanced Systems & Implementations",
                "skills": adv_missing if adv_missing else ["No gaps! Master: " + ", ".join(stages_config["Advanced"])]
            }

        # 4. Extract Resource Recommendations
        resource_repository = {}
        for skill in missing_required:
            if skill in resources_config:
                resource_repository[skill] = resources_config[skill]
                
        # 5. Priority Matrix
        priority_matrix = {
            "High": missing_required,
            "Medium": matched_required,
            "Low": additional_skills
        }
        
        # 6. Career Readiness Forecast (Deterministic base values)
        current_readiness = round(100 - gap_score, 1)
        projected_midpoint = round(current_readiness + (gap_score / 2), 1)
        projected_final = 100.0
        
        # 7. AI Roadmap Explanations and Assessment
        prompt = f"""
        You are a principal technical educator and career development specialist.
        Provide a customized roadmap guide and timeline forecast for a candidate transitioning to a '{target_role}'.
        
        Candidate's Core Profile:
        - Possessed Required Skills: {matched_required}
        - Missing Required Skills: {missing_required}
        - Additional Skills: {additional_skills}
        - Current Readiness: {current_readiness}% (based on deterministic skill match)
        
        Provide the following details in a JSON format:
        1. AI Roadmap Explanation: A brief, motivational commentary on why this roadmap is structured, why these specific missing skills are critical, and the expected training outcomes.
        2. Current Readiness Forecast: Comment on their current state of hireability.
        3. Projected Readiness: The expected hiring value at the midpoint of their roadmap.
        4. Estimated Readiness After Completion: What their hiring prospectus looks like after mastering the missing skills.
        """
        
        schema = """
        {
            "ai_roadmap_explanation": "Commentary on roadmap structure, skill significance, and learning outcomes (string)",
            "current_readiness_comment": "Brief comment on current hireability (string)",
            "projected_readiness_comment": "Expected readiness status and profile value at the midpoint (string)",
            "post_completion_readiness_comment": "Hireability projection and job application strategy post-completion (string)"
        }
        """
        
        ai_guidance = self.llm_service.generate_json(prompt, schema)
        
        # Default safety fallbacks
        default_keys = {
            "ai_roadmap_explanation": f"Focus on acquiring the missing skills ({', '.join(missing_required)}) to build competency in the '{target_role}' role.",
            "current_readiness_comment": "Your current profile has foundational components but missing core competencies.",
            "projected_readiness_comment": "At the midpoint, you will be capable of supporting basic role requirements.",
            "post_completion_readiness_comment": "Upon completion, you will be highly competitive for entry/mid-level positions."
        }
        for key, val in default_keys.items():
            if key not in ai_guidance:
                ai_guidance[key] = val
                
        # Consolidate results
        return {
            "target_role": target_role,
            "stages": stages_data,
            "timeline_months": timeline_months,
            "monthly_plan": monthly_plan,
            "priority_matrix": priority_matrix,
            "resource_repository": resource_repository,
            "forecast": {
                "current": current_readiness,
                "midpoint": projected_midpoint,
                "final": projected_final,
                "comments": ai_guidance
            }
        }
