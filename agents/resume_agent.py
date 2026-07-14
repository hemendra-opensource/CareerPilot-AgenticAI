import logging
from utils.llm_service import LLMService
from utils.pdf_parser import extract_text_from_pdf
from utils.resume_parser import ResumeParser
from utils.ats_scorer import ATSScorer

class ResumeAnalyzerAgent:
    """
    Orchestrates the entire resume processing pipeline.
    Coordinates text extraction, structured parsing, gap auditing, and feedback generation.
    """
    
    def __init__(self):
        self.llm_service = LLMService()
        self.parser = ResumeParser(self.llm_service)
        self.scorer = ATSScorer(self.llm_service)
        
    def analyze_resume(self, pdf_file) -> dict:
        """
        Parses and scores an uploaded PDF resume, returning detailed analysis and feedback.
        
        Args:
            pdf_file: File-like object (e.g. from st.file_uploader).
            
        Returns:
            A dictionary containing parsed resume details, completeness score,
            missing sections list, and deep ATS auditor feedback.
        """
        logging.info("Starting resume analysis pipeline.")
        
        # 1. Extract raw text from PDF
        raw_text = extract_text_from_pdf(pdf_file)
        
        # 2. Parse text into structured dictionary fields via Groq
        parsed_data = self.parser.parse(raw_text)
        
        # 3. Calculate rule-based completeness score & missing sections
        completeness_score, missing_sections = self.scorer.calculate_completeness(parsed_data)
        
        # 4. Generate AI-powered feedback & scores
        ats_analysis = self.scorer.analyze_ats_and_feedback(
            parsed_data=parsed_data,
            completeness_score=completeness_score,
            missing_sections=missing_sections
        )
        
        # Consolidate results
        result = {
            "parsed_data": parsed_data,
            "completeness_score": completeness_score,
            "missing_sections": missing_sections,
            "ats_analysis": ats_analysis
        }
        
        logging.info("Resume analysis completed successfully.")
        return result
