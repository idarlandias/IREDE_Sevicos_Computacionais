from pypdf import PdfReader
import sys


def read_pdf(file_path):
    try:
        reader = PdfReader(file_path)
        text = ""
        # Read the first 10 pages to get an overview without overflowing context
        for page in reader.pages[:10]:
            text += page.extract_text() + "\n"

        with open("pdf_content_analysis.txt", "w", encoding="utf-8") as f:
            f.write(text)
        print("PDF read successfully. Content saved to pdf_content_analysis.txt")
    except Exception as e:
        print(f"Error reading PDF: {e}")


if __name__ == "__main__":
    read_pdf("docs/Cloud_Native_DevOps_Microservices_Engineering.pdf")
