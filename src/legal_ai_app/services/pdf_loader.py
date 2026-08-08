import fitz


class PDFLoader:

    def load_pdf(self, pdf_path: str) -> str:
        """
        Read a PDF and return all text as a single string.
        """

        document = fitz.open(pdf_path)

        text = ""

        for page in document:
            text += page.get_text()

        document.close()

        return text