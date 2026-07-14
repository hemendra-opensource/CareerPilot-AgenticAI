from utils.llm_service import LLMService

class ATSScorer:
    """Calculates ATS scores and provides feedback on resume strength and missing content."""
    
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service
        
    def calculate_completeness(self, parsed_data: dict) -> tuple[int, list[str]]:
        """
        Calculates a completeness score (0-100) and identifies missing sections.
        
        Args:
            parsed_data: The structured resume dictionary.
            
        Returns:
            A tuple of (completeness_score, list_of_missing_sections).
        """
        missing_sections = []
        score = 0
        
        # 1. Contact Information (Name + Email or Phone)
        if parsed_data.get("name") and (parsed_data.get("email") or parsed_data.get("phone")):
            score += 15
        else:
            missing_sections.append("Contact Information")
            
        # 2. Skills
        if parsed_data.get("skills") and len(parsed_data["skills"]) > 0:
            score += 25
        else:
            missing_sections.append("Skills")
            
        # 3. Experience
        if parsed_data.get("experience") and len(parsed_data["experience"]) > 0:
            score += 25
        else:
            missing_sections.append("Experience")
            
        # 4. Education
        if parsed_data.get("education") and len(parsed_data["education"]) > 0:
            score += 15
        else:
            missing_sections.append("Education")
            
        # 5. Projects
        if parsed_data.get("projects") and len(parsed_data["projects"]) > 0:
            score += 10
        else:
            missing_sections.append("Projects")
            
        # 6. Certifications
        if parsed_data.get("certifications") and len(parsed_data["certifications"]) > 0:
            score += 10
        else:
            missing_sections.append("Certifications")
            
        return score, missing_sections

    def analyze_ats_and_feedback(self, parsed_data: dict, completeness_score: int, missing_sections: list[str]) -> dict:
        """
        Analyzes the resume details using LLM to generate ATS score, readability score,
        strengths, weaknesses, suggestions, and keyword analysis.
        
        Args:
            parsed_data: The parsed resume dictionary.
            completeness_score: Calculated structure score.
            missing_sections: List of sections found to be empty.
            
        Returns:
            A dictionary containing scores, summaries, lists of strengths/weaknesses and suggestions.
        """
        prompt = f"""
        You are an elite Applicant Tracking System (ATS) auditor and professional career coach.
        Review the following parsed resume details. Note that they scored {completeness_score}/100 in structural completeness, with missing sections: {', '.join(missing_sections) if missing_sections else 'None'}.
        
        Parsed Resume Details:
        {parsed_data}
        
        Analyze the resume and return:
        1. ATS Score (0-100): How compatible is the format/phrasing?
        2. Readability Score (0-100): How professional, clear, and impact-driven is the writing?
        3. Professional Summary: A concise overview of their candidate profile based on the details.
        4. Strengths: What sections, highlights, or achievements stand out?
        5. Weak Areas: What points are vague, lack impact, or lack metrics?
        6. Missing Keywords: What critical industry keywords/action verbs are missing for their skill set?
        7. Improvement Suggestions: Actionable points to rephrase bullet points or content.
        8. ATS Optimization Suggestions: Actionable layout or phrasing changes for ATS compliance.
        """
        
        schema = """
        {
            "ats_score": "Score from 0 to 100 (integer representing formatting compatibility and keyword match)",
            "readability_score": "Score from 0 to 100 (integer representing flow, style, grammar, and impact)",
            "resume_summary": "Concise professional candidate summary (string)",
            "strengths": ["List of strengths (array of strings)"],
            "weak_areas": ["List of weak points or vague statements (array of strings)"],
            "missing_keywords": ["Critical keywords or tech terms missing (array of strings)"],
            "improvement_suggestions": ["Actionable content edits (array of strings)"],
            "ats_optimization_suggestions": ["Actionable ATS compliance guidelines (array of strings)"]
        }
        """
        
        feedback = self.llm_service.generate_json(prompt, schema)
        
        # Set default structures in case of LLM parse failure
        default_keys = {
            "ats_score": 60,
            "readability_score": 60,
            "resume_summary": "No summary generated.",
            "strengths": [],
            "weak_areas": [],
            "missing_keywords": [],
            "improvement_suggestions": [],
            "ats_optimization_suggestions": []
        }
        for key, val in default_keys.items():
            if key not in feedback:
                feedback[key] = val
                
        return feedback
