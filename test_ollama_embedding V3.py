import requests
import json
import os
from tqdm import tqdm

# Ollama API endpoint for embedding
OLLAMA_API_URL = "http://localhost:11434/api/embed"

def generate_embedding_with_ollama(text):
    """
    Generate embedding vector for the given text using Ollama API.

    Parameters:
    text (str): Input text to generate embedding for.

    Returns:
    list or None: Returns the embedding vector as a list if successful, otherwise None.
    """
    MAX_TEXT_LENGTH = 500  # Adjust this based on API limits
    if len(text) > MAX_TEXT_LENGTH:
        text = text[:MAX_TEXT_LENGTH]

    payload = {
        "model": "llama3:latest",
        "input": text
    }

    try:
        response = requests.post(OLLAMA_API_URL, json=payload)
        if response.status_code == 200:
            data = response.json()
            embeddings = data.get("embeddings", [])
            if embeddings:
                return embeddings[0]
        else:
            print(f"Error: Status code {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return None

def load_json(file_path):
    """
    Load JSON data from a file.

    Parameters:
    file_path (str): Path to the JSON file.

    Returns:
    dict: Parsed JSON data.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(data, output_file):
    """
    Save data to a JSON file.

    Parameters:
    data (dict): Data to save.
    output_file (str): Path to the output JSON file.
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def vectorize_sentences(input_json_path, output_json_path):
    """
    Vectorize sentences in the JSON file using Ollama API and save the embeddings.

    Parameters:
    input_json_path (str): Path to the input JSON file.
    output_json_path (str): Path to the output JSON file.
    """
    # Load input JSON
    data = load_json(input_json_path)

    embeddings_output = []

    for doc in tqdm(data, desc="Processing documents"):
        title = doc.get('title', '')
        paragraph = doc.get('paragraph', '')
        sentences = doc.get('sentences', [])
        tables = doc.get('tables', [])

        for sentence in sentences:
            if sentence:
                embedding = generate_embedding_with_ollama(sentence)
                if embedding:
                    embeddings_output.append({
                        'title': title,
                        'paragraph': paragraph,
                        'sentence': sentence,
                        'embedding': embedding,
                        'tables': tables
                    })

    # Save embeddings to the output JSON
    save_json(embeddings_output, output_json_path)

if __name__ == "__main__":
    # Input file path (JSON file to vectorize)
    input_file = r"G:\966175\Cleantext\wn.json"
    # Output file path (where to save the embeddings)
    output_file = r"G:\966175\embeddings_split\wn_embeddings.json"

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Run the vectorization process
    vectorize_sentences(input_file, output_file)
    print(f"Embeddings saved to {output_file}")
