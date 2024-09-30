import os
import json
import requests

# Input JSON file containing the processed documents
INPUT_FILE = 'processed_documents.json'

# Output JSON file to save the embeddings
EMBEDDINGS_FILE = 'document_embeddings.json'

# Ollama API endpoint for embeddings
OLLAMA_API_URL = "http://localhost:11434/api/embed"

def load_processed_documents(input_file):

    with open(input_file, 'r', encoding='utf-8') as f:
        documents = json.load(f)
    return documents

def generate_embedding_with_ollama(text):

    payload = {
        "model": "llama3:latest",
        "input": text
    }

    try:
        response = requests.post(OLLAMA_API_URL, json=payload)
        if response.status_code == 200:
            data = response.json()
            embedding = data.get("embedding")
            if embedding:
                return embedding
            else:
                print("Embeddings not found in the response.")
                return None
        else:
            print(f"Error: Received status code {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"An exception occurred: {e}")
        return None

def generate_embeddings(documents):

    embeddings = []
    for idx, item in enumerate(documents):
        title = item['title']
        text = item['text']
        print(f"Generating embedding for: {title} ({idx+1}/{len(documents)})")
        embedding = generate_embedding_with_ollama(text)
        if embedding is not None:
            embeddings.append({
                'title': title,
                'text': text,
                'embedding': embedding
            })
        else:
            print(f"Failed to generate embedding for: {title}")
    return embeddings

def save_embeddings(embeddings, embeddings_file):

    with open(embeddings_file, 'w', encoding='utf-8') as f:
        json.dump(embeddings, f, ensure_ascii=False, indent=2)
    print(f"Embeddings saved to {embeddings_file}")

if __name__ == "__main__":
    # Check if embeddings file exists
    if not os.path.exists(EMBEDDINGS_FILE):
        # Load the processed documents
        documents = load_processed_documents(INPUT_FILE)
        # Generate embeddings for each document
        embeddings = generate_embeddings(documents)
        # Save the embeddings to a file
        save_embeddings(embeddings, EMBEDDINGS_FILE)
    else:
        print(f"Embeddings file '{EMBEDDINGS_FILE}' already exists.")
