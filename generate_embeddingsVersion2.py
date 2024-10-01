import requests
import json
import traceback
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
    print("Starting generate_embedding_with_ollama function...")  # Confirm function start

    # Truncate text if it exceeds the maximum length
    MAX_TEXT_LENGTH = 500  # Adjust according to API limitations
    if len(text) > MAX_TEXT_LENGTH:
        print(f"Text length ({len(text)}) exceeds maximum allowed ({MAX_TEXT_LENGTH}). Truncating text.")
        text = text[:MAX_TEXT_LENGTH]

    # Request payload
    payload = {
        "model": "llama3:latest",
        "input": text
    }

    try:
        print("Sending POST request to Ollama API...")  # Confirm request send
        # Send POST request to Ollama API
        response = requests.post(OLLAMA_API_URL, json=payload)

        # Print status code and response text
        print(f"Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")

        if response.status_code == 200:
            try:
                data = response.json()
                print("Response JSON parsed successfully.")
            except json.JSONDecodeError as e:
                print(f"JSONDecodeError: {e}")
                print(f"Response Text: {response.text}")
                return None

            print(f"Data type: {type(data)}")
            print(f"Available keys in response data: {list(data.keys())}")

            embeddings = data.get("embeddings")
            print(f"Type of embeddings: {type(embeddings)}")

            if embeddings:
                if isinstance(embeddings, list) and len(embeddings) > 0:
                    embedding = embeddings[0]
                    print("Successfully generated embeddings!")
                    print(f"Embedding length: {len(embedding)}")
                    return embedding
                else:
                    print("Embeddings are empty or not in the expected format.")
                    return None
            else:
                print("Embeddings not found in the response.")
                print(f"Response Text: {response.text}")
                return None
        else:
            print(f"Error: Received status code {response.status_code}")
            print(f"Response Text: {response.text}")
            return None
    except Exception as e:
        print(f"An exception occurred: {e}")
        traceback.print_exc()
        return None

def load_json(file_path):
    """
    Load JSON data from a file.

    Parameters:
    file_path (str): Path to the JSON file.

    Returns:
    list: List of document entries.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def save_json(data, file_path):
    """
    Save data to a JSON file.

    Parameters:
    data (list): List of data entries to save.
    file_path (str): Path to the output JSON file.
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def main():
    """
    Main function to vectorize sentences using the local Ollama API.
    """
    # Path to the processed documents JSON file
    input_file = r"G:\966175\processed_documents.json"

    # Path to save the embeddings JSON file
    output_file = r"G:\966175\embeddings.json"

    # Check if the input file exists
    if not os.path.exists(input_file):
        print(f"File not found: {input_file}")
        return

    # Load processed documents from JSON file
    print("Loading processed_documents.json...")
    with open(input_file, 'r', encoding='utf-8') as f:
        documents = json.load(f)

    embeddings = []
    total_sentences = sum(len(doc.get('sentences', [])) for doc in documents)
    print(f"Total sentences to process: {total_sentences}")

    # Iterate through each document and its sentences
    for idx, doc in enumerate(tqdm(documents, desc="Processing documents")):
        title = doc.get('title', '')
        paragraph = doc.get('paragraph', '')
        sentences = doc.get('sentences', [])
        tables = doc.get('tables', [])

        for sentence in sentences:
            if not sentence:
                print(f"Empty sentence in document {idx}. Skipping.")
                continue

            print(f"Processing sentence: {sentence[:50]}...")  # Print first 50 chars for brevity
            embedding = generate_embedding_with_ollama(sentence)
            if embedding:
                embeddings.append({
                    'title': title,
                    'paragraph': paragraph,
                    'sentence': sentence,
                    'embedding': embedding,
                    'tables': tables  # Include associated tables if needed
                })
                print(f"Successfully generated embedding for sentence.")
            else:
                print(f"Failed to generate embedding for sentence.")

    # Save embeddings to a JSON file
    print(f"Saving embeddings to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(embeddings, f, ensure_ascii=False, indent=4)

    print(f"Embeddings successfully saved to {output_file}")

if __name__ == "__main__":
    main()
