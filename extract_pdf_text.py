# file: pdf_to_text.py
# Required package: PyPDF2
# pip install PyPDF2

import sys
import PyPDF2

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

def extract_text(pdf_file, output_txt="book_text.txt"):
    text = ""
    try:
        reader = PyPDF2.PdfReader(pdf_file)
    except Exception as e:
        print(f"❌ Error opening PDF: {e}")
        return

    for i, page in enumerate(reader.pages):
        try:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
            else:
                print(f"⚠️ Warning: Page {i+1} had no extractable text")
        except Exception as e:
            print(f"❌ Error reading page {i+1}: {e}")

    # Save extracted text
    try:
        with open(output_txt, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"✅ PDF text extracted and saved as {output_txt}")
    except Exception as e:
        print(f"❌ Error saving text file: {e}")

if __name__ == "__main__":
    pdf_file = "uploaded_book.pdf"  # Change to your PDF filename
    extract_text(pdf_file)
