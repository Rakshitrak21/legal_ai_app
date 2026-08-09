import fitz


class PDFLoader:

    def load_pages(self, file_path: str):

        pdf = fitz.open(file_path)

        pages = []

        for page_number, page in enumerate(pdf, start=1):

            text = page.get_text()

            if text.strip():
                pages.append({
                    "page": page_number,
                    "text": text,
                })

        pdf.close()

        return pages

    def load_pdf(self, file_path: str):

        pages = self.load_pages(file_path)

        return "\n\n".join(
            page["text"]
            for page in pages
        )