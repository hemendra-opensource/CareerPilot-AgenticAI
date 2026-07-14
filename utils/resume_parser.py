from utils.llm_service import LLMService

class ResumeParser:
    """Parses raw resume text into structured professional profiles using LLMService."""
    
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service
        
    def parse(self, resume_text: str) -> dict:
        """
        Parses raw resume text into a structured dictionary.
        
        Args:
            resume_text: The full raw text of the resume.
            
        Returns:
            A dictionary containing name, email, phone, skills, education,
            certifications, projects, and work experience.
        """
        prompt = f"""
        You are an expert resume parsing model. Your job is to extract candidate details from the raw resume text provided below.
        Be thorough and capture all entries. Extract details exactly as stated, but clean up spacing where necessary.
        
        Resume Text:
        ---
        {resume_text}
        ---
        """
        
        schema = """
        {
            "name": "Full name of the candidate (string, default empty string if missing)",
            "email": "Email address (string, default empty string if missing)",
            "phone": "Phone number (string, default empty string if missing)",
            "skills": ["List of core technical or soft skills extracted (array of strings)"],
            "education": [
                {
                    "institution": "University, college, or school name (string)",
                    "degree": "Degree or program name (string)",
                    "year": "Graduation year or date range (string)"
                }
            ],
            "certifications": ["List of certifications, credentials, or licenses (array of strings)"],
            "projects": [
                {
                    "title": "Project title (string)",
                    "description": "Short explanation of the project accomplishments, tasks, or tech stack (string)"
                }
            ],
            "experience": [
                {
                    "company": "Company or organization name (string)",
                    "role": "Job title or role (string)",
                    "duration": "Employment dates or duration (string)",
                    "description": "Key responsibilities, projects, or accomplishments (string)"
                }
            ]
        }
        """
        
        parsed_data = self.llm_service.generate_json(prompt, schema)
        
        # Add basic fallbacks in case key extractions are empty
        default_keys = {
            "name": "", "email": "", "phone": "",
            "skills": [], "education": [], "certifications": [],
            "projects": [], "experience": []
        }
        for key, val in default_keys.items():
            if key not in parsed_data:
                parsed_data[key] = val
                
        return parsed_data
