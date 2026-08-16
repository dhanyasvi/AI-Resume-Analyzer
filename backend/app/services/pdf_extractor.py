import fitz


def extract_pdf_text(pdf_bytes: bytes) -> str:
    """Extract selectable text from a PDF stored in memory."""
    try:
        document = fitz.open(stream=pdf_bytes, filetype="pdf")
        text = "\n".join(page.get_text("text") for page in document)
        document.close()
    except Exception as error:
        raise ValueError("We could not read this PDF. Please upload a valid PDF file.") from error

    cleaned_text = "\n".join(line.strip() for line in text.splitlines() if line.strip())
    if not cleaned_text:
        raise ValueError("No selectable text was found. This may be a scanned resume; OCR support will be added later.")
    return cleaned_text
