import PyPDF2

def extract_text_from_pdf(file_path: str) -> str:
    """
    Opens a PDF file and returns all text as a single string.
    """
    text_content = []
    try:
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            # Iterate over all pages
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    text_content.append(text)
        
        return "\n".join(text_content)
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""