# Required package: PyPDF2
# pip install PyPDF2
import sys
sys.stdout.reconfigure(encoding='utf-8')
import PyPDF2

def extract_text(pdf_file, output_txt="book_text.txt"):
    text = ""
    reader = PyPDF2.PdfReader(pdf_file)
    for page in reader.pages:
        text += page.extract_text() + "\n"

    # Save extracted text
    with open(output_txt, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"✅ PDF text extracted and saved as {output_txt}")

if __name__ == "__main__":
    pdf_file = "uploaded_book.pdf"  # Change to your PDF filename
    extract_text(pdf_file)
