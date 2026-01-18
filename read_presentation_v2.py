import pdfplumber


def read_pdf(file_path):
    try:
        with pdfplumber.open(file_path) as pdf:
            text = ""
            for page in pdf.pages[:5]:  # Read first 5 pages
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"

        with open("pdf_content_analysis_v2.txt", "w", encoding="utf-8") as f:
            f.write(text)
        print("PDF read successfully using pdfplumber.")
    except Exception as e:
        print(f"Error reading PDF: {e}")


if __name__ == "__main__":
    read_pdf("docs/Cloud_Native_DevOps_Microservices_Engineering.pdf")
