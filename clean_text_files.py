import pdfplumber
import re
import spacy
import json
import os
import sys

def extract_text_and_tables_from_pdf(pdf_path):
    content = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            num_pages = len(pdf.pages)
            print(f'Total pages in PDF: {num_pages}')

            for i in range(num_pages):
                print(f'Processing page {i + 1} of {num_pages}...')
                try:
                    page = pdf.pages[i]
                    page_text = page.extract_text()
                    page_tables = page.extract_tables()
                except Exception as e:
                    print(f'Error extracting page {i + 1}: {e}')
                    page_text = ''
                    page_tables = []

                page_content = {
                    'page_number': i + 1,
                    'text': page_text,
                    'tables': page_tables
                }
                content.append(page_content)
    except FileNotFoundError:
        print(f'File not found: {pdf_path}')
    except Exception as e:
        print(f'Error opening {pdf_path}: {e}')
    return content

def parse_document_structure(content):
    document = []
    current_section = None
    heading_pattern = re.compile(r'^\s*(\d+(\.\d+)*)\s+(.+)', re.MULTILINE)

    for page in content:
        page_number = page['page_number']
        page_text = page['text']
        page_tables = page['tables']

        if not page_text:
            continue

        lines = page_text.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Check if the line matches a heading
            match = heading_pattern.match(line)
            if match:
                # If a new heading is found, create a new section
                title_number = match.group(1)
                title_text = match.group(3).strip()
                current_title = f"{title_number} {title_text}"

                current_section = {
                    'title': current_title,
                    'content': '',
                    'tables': []
                }
                document.append(current_section)
                continue

            # If a current section exists, append the line to its content
            if current_section:
                current_section['content'] += line + ' '

        # Associate tables with the current section
        if current_section and page_tables:
            for table in page_tables:
                # Convert table to a string representation, handling None values
                try:
                    table_text = '\n'.join(['\t'.join([cell if cell is not None else '' for cell in row]) for row in table])
                    current_section['tables'].append(table_text)
                except Exception as e:
                    print(f'Error processing table on page {page_number}: {e}')
                    continue

    return document

def split_paragraphs_and_sentences(document, nlp):
    processed_data = []
    for section in document:
        title = section['title']
        content = section['content']
        tables = section['tables']

        # Split content into paragraphs based on two or more spaces
        paragraphs = re.split(r'\s{2,}', content)
        paragraphs = [para.strip() for para in paragraphs if para.strip()]

        for para in paragraphs:
            # Use spaCy to split paragraphs into sentences
            doc = nlp(para)
            sentences = [sent.text.strip() for sent in doc.sents]

            processed_data.append({
                'title': title,
                'paragraph': para,
                'sentences': sentences,
                'tables': tables  # Include tables associated with this section
            })
    return processed_data

def main():
    # Load spaCy language model for English documents
    try:
        nlp = spacy.load('en_core_web_sm')
    except OSError:
        print("spaCy English model not found. Downloading...")
        os.system("python -m spacy download en_core_web_sm")
        try:
            nlp = spacy.load('en_core_web_sm')
        except Exception as e:
            print(f'Error loading spaCy model after download: {e}')
            sys.exit(1)

    # Directory containing PDF files
    pdf_directory = r'G:\966175\712038\PDF DEL'  # Update to your PDF directory path
    output_file = r'G:\966175\processed_documents.json'

    if not os.path.exists(pdf_directory):
        print(f"Directory does not exist: {pdf_directory}")
        sys.exit(1)

    all_documents = []

    # Iterate through all PDF files in the directory
    for filename in os.listdir(pdf_directory):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(pdf_directory, filename)
            print(f'Processing file: {pdf_path}')
            content = extract_text_and_tables_from_pdf(pdf_path)
            if not content:
                print(f'No content extracted from {pdf_path}. Skipping.')
                continue

            document_structure = parse_document_structure(content)
            if not document_structure:
                print(f'No document structure found in {pdf_path}. Skipping.')
                continue

            processed_data = split_paragraphs_and_sentences(document_structure, nlp)
            all_documents.extend(processed_data)

    if all_documents:
        # Save the processed data to a JSON file
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(all_documents, f, ensure_ascii=False, indent=4)
            print(f'Processing completed. Data saved to: {output_file}')
        except Exception as e:
            print(f'Error saving JSON file: {e}')
    else:
        print('No documents processed. Please check your PDF files and parsing logic.')

if __name__ == '__main__':
    main()
