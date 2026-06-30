from PyPDF2 import PdfReader

def extract_text(file):
    if file.filename.endswith(".txt"):
        content = file.file.read()
        return content.decode("utf-8")

    elif file.filename.endswith(".pdf"):
        reader = PdfReader(file.file)
        text=""
        for page in reader.pages:
            text += page.extract_text()
        return text

    else:
        raise Exception("Invalid file type")