import fitz  # PyMuPDF
import os
import json

# Directory containing the PDF files
PDF_DIR = r"G:\966175\712038\pdf"

# Output JSON file to save the extracted structured text
OUTPUT_FILE = 'processed_documents.json'

def extract_text_with_structure(pdf_path):

    doc = fitz.open(pdf_path)
    toc = doc.get_toc()  # Get the table of contents
    content = []

    if not toc:
        # If there's no table of contents, extract the full text
        full_text = ""
        for page in doc:
            full_text += page.get_text()
        content.append({'title': 'Full Document', 'text': full_text.strip()})
    else:
        # If there's a table of contents, extract text based on chapters
        for idx, entry in enumerate(toc):
            level, title, page_num = entry
            start_page = page_num - 1  # Page numbers start from 0
            end_page = doc.page_count - 1  # Default end page is the last page

            # Determine the end page for the current chapter
            for next_entry in toc[idx + 1:]:
                next_level, _, next_page_num = next_entry
                if next_level <= level:
                    end_page = next_page_num - 2  # End at the page before the next same/higher level chapter
                    break

            # Extract text for the current chapter
            chapter_text = ""
            for page in range(start_page, end_page + 1):
                chapter_text += doc.load_page(page).get_text()
            content.append({'title': title, 'text': chapter_text.strip()})
    return content

def process_pdfs(pdf_dir):
    documents = []
    for filename in os.listdir(pdf_dir):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(pdf_dir, filename)
            print(f"Processing {pdf_path}...")
            chapters = extract_text_with_structure(pdf_path)
            documents.extend(chapters)
    return documents

def save_processed_documents(documents, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(documents, f, ensure_ascii=False, indent=2)
    print(f"Processed documents saved to {output_file}")

if __name__ == "__main__":
    # Process the PDFs and extract structured text
    processed_documents = process_pdfs(PDF_DIR)
    # Save the processed documents to a JSON file
    save_processed_documents(processed_documents, OUTPUT_FILE)
