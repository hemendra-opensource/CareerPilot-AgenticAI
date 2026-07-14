from utils.llm_service import LLMService
from utils.role_database import ROLE_DATABASE

class SkillMatcher:
    """Helper to perform case-insensitive skill matching using Python sets."""
    
    @staticmethod
    def match_skills(candidate_skills: list[str], required_skills: list[str]) -> dict:
        """
        Determines matched, missing, and additional skills case-insensitively.
        
        Args:
            candidate_skills: List of skills possessed by the candidate.
            required_skills: List of skills required for the target role.
            
        Returns:
            A dictionary containing matched_skills, missing_skills, additional_skills, and gap_score.
        """
        # Create case-insensitive mappings to preserve original casing in outputs
        cand_map = {s.lower().strip(): s.strip() for s in candidate_skills if s.strip()}
        req_map = {s.lower().strip(): s.strip() for s in required_skills if s.strip()}
        
        cand_set = set(cand_map.keys())
        req_set = set(req_map.keys())
        
        matched_keys = cand_set.intersection(req_set)
        missing_keys = req_set.difference(cand_set)
        additional_keys = cand_set.difference(req_set)
        
        matched_skills = [req_map[k] for k in matched_keys]
        missing_skills = [req_map[k] for k in missing_keys]
        additional_skills = [cand_map[k] for k in additional_keys]
        
        total_required = len(required_skills)
        gap_score = (len(missing_skills) / total_required * 100) if total_required > 0 else 0.0
        
        return {
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "additional_skills": additional_skills,
            "gap_score": round(gap_score, 1)
        }

class SkillGapAgent:
    """Orchestrates skill gap analysis comparing candidate skills to target role requirements."""
    
    def __init__(self):
        self.llm_service = LLMService()
        
    def analyze_gaps(self, candidate_skills: list[str], target_role: str) -> dict:
        """
        Compares candidate skills against required role skills and calls Groq for advice.
        
        Args:
            candidate_skills: List of skills extracted or input.
            target_role: The selected role target (e.g. Data Scientist).
            
        Returns:
            A dictionary containing matching arrays, gap score, and qualitative advice.
        """
        if target_role not in ROLE_DATABASE:
            raise ValueError(f"Target role '{target_role}' not found in role database.")
            
        required_skills = ROLE_DATABASE[target_role]
        
        # Calculate matching sets deterministically
        match_result = SkillMatcher.match_skills(candidate_skills, required_skills)
        
        # Query LLM for career development suggestions
        prompt = f"""
        You are a seasoned career development strategist and technical recruiter. 
        Review this skill gap analysis for a candidate aiming to transition to a '{target_role}' role.
        
        Candidate's Matched Required Skills: {match_result["matched_skills"]}
        Candidate's Missing Required Skills: {match_result["missing_skills"]}
        Candidate's Additional Skills (Not required but possessed): {match_result["additional_skills"]}
        Skill Gap Score: {match_result["gap_score"]}% (0% represents a complete match, 100% represents a complete gap)
        
        Provide professional, constructive feedback in the following format:
        1. Career Readiness Summary: A high-level overview of their alignment and readiness.
        2. Top 5 Skills to Learn: A list of the most critical skills to focus on next.
        3. Recommended Learning Sequence: A structured, step-by-step roadmap to acquire the missing skills.
        4. Hiring Readiness Assessment: A realistic evaluation of their current chances of landing this role and milestones to aim for.
        """
        
        schema = """
        {
            "career_readiness_summary": "Concise summary of candidate's career readiness for the target role (string)",
            "top_skills_to_learn": ["Skill 1", "Skill 2", "Skill 3", "Skill 4", "Skill 5"],
            "learning_sequence": ["Step 1: Description", "Step 2: Description", ...],
            "hiring_readiness_assessment": "Realistic rating of hireability and milestone objectives (string)"
        }
        """
        
        advice = self.llm_service.generate_json(prompt, schema)
        
        # Default safety fallbacks
        default_keys = {
            "career_readiness_summary": "Unable to generate readiness summary.",
            "top_skills_to_learn": match_result["missing_skills"][:5] if match_result["missing_skills"] else ["No missing skills!"],
            "learning_sequence": [f"Learn {skill}" for skill in match_result["missing_skills"]],
            "hiring_readiness_assessment": "Hiring assessment unavailable."
        }
        for key, val in default_keys.items():
            if key not in advice:
                advice[key] = val
                
        return {
            "target_role": target_role,
            "required_skills": required_skills,
            "matched_skills": match_result["matched_skills"],
            "missing_skills": match_result["missing_skills"],
            "additional_skills": match_result["additional_skills"],
            "gap_score": match_result["gap_score"],
            "advice": advice
        }
