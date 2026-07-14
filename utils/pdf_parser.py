import PyPDF2
import logging

def extract_text_from_pdf(pdf_file) -> str:
    """
    Extracts text from an uploaded PDF file or file-like object.
    Supports multi-page PDFs and cleans empty outputs.
    
    Args:
        pdf_file: File-like object (e.g. from st.file_uploader) or path to a PDF file.
        
    Returns:
        The extracted text as a single string.
        
    Raises:
        ValueError: If the file is corrupted, empty, or lacks readable text.
    """
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        
        for i, page in enumerate(reader.pages):
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
                
        cleaned_text = text.strip()
        if not cleaned_text:
            raise ValueError(
                "No readable text found in the PDF. The file may be empty, password-protected, "
                "or contain only scanned images without OCR."
            )
            
        return cleaned_text
        
    except Exception as e:
        logging.error(f"Failed to parse PDF document: {str(e)}")
        raise ValueError(f"Failed to parse PDF document: {str(e)}")
