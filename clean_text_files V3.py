import pdfplumber
import re
import json
import os

def extract_text_and_tables_from_pdf(pdf_path):
    """
    Extract text and tables from a PDF file using pdfplumber.

    Parameters:
    pdf_path (str): Path to the PDF file.

    Returns:
    list: A list of dictionaries containing page number, text, and tables.
    """
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
                    'text': page_text.strip() if page_text else '',
                    'tables': page_tables
                }
                content.append(page_content)
    except FileNotFoundError:
        print(f'File not found: {pdf_path}')
    except Exception as e:
        print(f'Error opening {pdf_path}: {e}')
    return content

def clean_and_split_sentences(text):
    """
    Clean and split text into sentences, removing unnecessary punctuation and spaces.

    Parameters:
    text (str): The raw text.

    Returns:
    list: A list of cleaned sentences.
    """
    # Replace multiple spaces or unnecessary punctuation
    cleaned_text = re.sub(r'\s*\.\s*', '.', text)  # Remove spaces around periods
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()  # Collapse multiple spaces

    # Split sentences based on periods
    sentences = re.split(r'(?<=\w\.)\s+', cleaned_text)
    return sentences

def parse_document_structure(content):
    """
    Parse the document structure to identify titles, sections, paragraphs, and handle tables.

    Parameters:
    content (list): List of dictionaries containing page number, text, and tables.

    Returns:
    list: A list of structured data with titles, paragraphs, sentences, and tables.
    """
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
                    'paragraph': '',
                    'sentences': [],
                    'tables': []
                }
                document.append(current_section)
                continue

            # If a current section exists, append the cleaned and split sentences to its content
            if current_section:
                cleaned_sentences = clean_and_split_sentences(line)
                current_section['sentences'].extend(cleaned_sentences)

        # Associate tables with the current section
        if current_section and page_tables:
            for table in page_tables:
                # Convert table to a string representation, handling None values
                try:
                    table_text = '\n'.join(['\t'.join([cell if cell is not None else '' for cell in row]) for row in table])
                    current_section['tables'].append(table_text)
                except Exception as e:
                    print(f'Error processing table on page {page_number}: {e}')

    return document

def save_to_json(data, output_file):
    """
    Save the structured data to a JSON file.

    Parameters:
    data (list): Structured data to be saved.
    output_file (str): Path to the output JSON file.
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f'Processed text saved to {output_file}')

def main():
    # Update the PDF path and output JSON path as per your setup
    pdf_directory = r"G:\966175\712038\PDFDEL"
    output_directory = r"G:\966175\Cleantext"
    
    # Create output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    for filename in os.listdir(pdf_directory):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(pdf_directory, filename)
            output_file = os.path.join(output_directory, f"{os.path.splitext(filename)[0]}.json")

            print(f'Processing {pdf_path}...')
            
            # Extract text and tables from the PDF
            content = extract_text_and_tables_from_pdf(pdf_path)

            # Parse the document structure
            document_structure = parse_document_structure(content)

            # Save the structured data to JSON
            save_to_json(document_structure, output_file)

if __name__ == "__main__":
    main()
import pdfplumber
import re
import json
import os

def extract_text_and_tables_from_pdf(pdf_path):
    """
    Extract text and tables from a PDF file using pdfplumber.

    Parameters:
    pdf_path (str): Path to the PDF file.

    Returns:
    list: A list of dictionaries containing page number, text, and tables.
    """
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
                    'text': page_text.strip() if page_text else '',
                    'tables': page_tables
                }
                content.append(page_content)
    except FileNotFoundError:
        print(f'File not found: {pdf_path}')
    except Exception as e:
        print(f'Error opening {pdf_path}: {e}')
    return content

def clean_and_split_sentences(text):
    """
    Clean and split text into sentences, removing unnecessary punctuation and spaces.

    Parameters:
    text (str): The raw text.

    Returns:
    list: A list of cleaned sentences.
    """
    # Replace multiple spaces or unnecessary punctuation
    cleaned_text = re.sub(r'\s*\.\s*', '.', text)  # Remove spaces around periods
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()  # Collapse multiple spaces

    # Split sentences based on periods
    sentences = re.split(r'(?<=\w\.)\s+', cleaned_text)
    return sentences

def parse_document_structure(content):
    """
    Parse the document structure to identify titles, sections, paragraphs, and handle tables.

    Parameters:
    content (list): List of dictionaries containing page number, text, and tables.

    Returns:
    list: A list of structured data with titles, paragraphs, sentences, and tables.
    """
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
                    'paragraph': '',
                    'sentences': [],
                    'tables': []
                }
                document.append(current_section)
                continue

            # If a current section exists, append the cleaned and split sentences to its content
            if current_section:
                cleaned_sentences = clean_and_split_sentences(line)
                current_section['sentences'].extend(cleaned_sentences)

        # Associate tables with the current section
        if current_section and page_tables:
            for table in page_tables:
                # Convert table to a string representation, handling None values
                try:
                    table_text = '\n'.join(['\t'.join([cell if cell is not None else '' for cell in row]) for row in table])
                    current_section['tables'].append(table_text)
                except Exception as e:
                    print(f'Error processing table on page {page_number}: {e}')

    return document

def save_to_json(data, output_file):
    """
    Save the structured data to a JSON file.

    Parameters:
    data (list): Structured data to be saved.
    output_file (str): Path to the output JSON file.
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f'Processed text saved to {output_file}')

def main():
    # Update the PDF path and output JSON path as per your setup
    pdf_directory = r"G:\966175\712038\PDFDEL"
    output_directory = r"G:\966175\Cleantext"
    
    # Create output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    for filename in os.listdir(pdf_directory):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(pdf_directory, filename)
            output_file = os.path.join(output_directory, f"{os.path.splitext(filename)[0]}.json")

            print(f'Processing {pdf_path}...')
            
            # Extract text and tables from the PDF
            content = extract_text_and_tables_from_pdf(pdf_path)

            # Parse the document structure
            document_structure = parse_document_structure(content)

            # Save the structured data to JSON
            save_to_json(document_structure, output_file)

if __name__ == "__main__":
    main()
