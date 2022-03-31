import PyPDF2
import docx


def process(file_type, file_path):
    if file_type == 0:
        doc = docx.Document(file_path)
        paragraphs = doc.paragraphs
        for para in paragraphs:
            print(para.text)

    elif file_type == 1:
        with open(file_path, 'rb') as f:
            pdf = PyPDF2.PdfFileReader(f)
            print(pdf.getDocumentInfo())
            for page in range(pdf.numPages):
                pageObj = pdf.getPage(page)
                text = pageObj.extractText()
                print(text)
            f.close()
