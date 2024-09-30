import requests
import json
import traceback
import os

# Ollama API endpoint for embedding
OLLAMA_API_URL = "http://localhost:11434/api/embed"

def generate_embedding_with_ollama(text):
    # Truncate text if it exceeds the maximum length
    MAX_TEXT_LENGTH = 500  # Adjust according to API limitations
    if len(text) > MAX_TEXT_LENGTH:
        text = text[:MAX_TEXT_LENGTH]

    # Request payload
    payload = {
        "model": "llama3:latest",
        "input": text
    }

    try:
        # Send POST request to Ollama API
        response = requests.post(OLLAMA_API_URL, json=payload)

        if response.status_code == 200:
            data = response.json()
            embeddings = data.get("embeddings")
            if embeddings and isinstance(embeddings, list) and len(embeddings) > 0:
                embedding = embeddings[0]
                return embedding
            else:
                return None
        else:
            return None
    except Exception as e:
        print(f"An exception occurred: {e}")
        traceback.print_exc()
        return None

def main():
    # Path to the processed documents JSON file
    file_path = r"G:\966175\processed_documents.json"

    # Check if file exists
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    # Load processed documents from JSON file
    with open(file_path, 'r', encoding='utf-8') as f:
        documents = json.load(f)

    embeddings = []
    for idx, doc in enumerate(documents):
        title = doc.get('title', '')
        text = doc.get('text', '')
        if not text:
            print(f"Document {idx} has no content. Skipping.")
            continue

        # Split the text into paragraphs
        paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
        for para_idx, paragraph in enumerate(paragraphs):
            print(f"Processing document {idx}, paragraph {para_idx}...")
            embedding = generate_embedding_with_ollama(paragraph)
            if embedding:
                embeddings.append({
                    'doc_id': idx,
                    'para_id': para_idx,
                    'title': title,
                    'text': paragraph,
                    'embedding': embedding
                })
                print(f"Successfully generated embedding for document {idx}, paragraph {para_idx}.")
            else:
                print(f"Failed to generate embedding for document {idx}, paragraph {para_idx}.")

    # Save embeddings to a JSON file
    output_file = r"G:\966175\paragraph_embeddings.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(embeddings, f, ensure_ascii=False, indent=4)

    print(f"Embeddings saved to {output_file}")

if __name__ == "__main__":
    main()
