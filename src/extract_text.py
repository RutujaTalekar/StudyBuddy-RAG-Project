import fitz  # PyMuPDF
import json
import os

PDF_PATH = "data/Alex-Xu-SysDesignHandbook.pdf"
OUTPUT_PATH = "data/book_pages.json"

def extract_pages(pdf_path):
    doc = fitz.open(pdf_path)
    pages = []

    for i, page in enumerate(doc):
        text = page.get_text()
        if text.strip():  # skip blank pages
            pages.append({
                "page_number": i + 1,
                "content": text.strip()
            })

    return pages

if __name__ == "__main__":
    if not os.path.exists(PDF_PATH):
        print(f"❌ PDF not found at {PDF_PATH}")
    else:
        print(f"📖 Extracting from: {PDF_PATH}")
        pages = extract_pages(PDF_PATH)

        with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
            json.dump(pages, f, indent=2, ensure_ascii=False)

        print(f"✅ Extracted {len(pages)} pages. Saved to {OUTPUT_PATH}")
