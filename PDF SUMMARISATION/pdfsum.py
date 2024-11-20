import requests
import faiss
import numpy as np
from PyPDF2 import PdfReader
import streamlit as st

# Cohere API URL
COHERE_API_URL = "https://api.cohere.ai/v1/embed"
COHERE_API_KEY = "sDg06pJA57ZfkA6BFgayTLRZuMcRQ1IUKzVwyqLl"  # Replace with your Cohere API key

# Step 1: Extract text from PDF
def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Step 2: Split text into chunks
def split_text_into_chunks(text, chunk_size=300):
    words = text.split()
    chunks = [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
    return chunks

# Step 3: Create embeddings using Cohere API
def create_embeddings(chunks):
    headers = {
        "Authorization": f"Bearer {COHERE_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "texts": chunks,
        "model": "embed-english-light-v2.0"
    }

    response = requests.post(COHERE_API_URL, headers=headers, json=data)

    if response.status_code == 200:
        return np.array(response.json()['embeddings'])
    else:
        raise Exception(f"Error embedding text: {response.text}")

# Step 4: Build a FAISS vector store
def build_faiss_index(embeddings, chunks):
    dimension = embeddings.shape[1]  # Get the dimension of the embeddings
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return index, chunks

# Step 5: Retrieve relevant chunks
def retrieve_relevant_chunks(query, index, chunks, top_k=3):
    query_embedding = np.array(create_embeddings([query]))
    distances, indices = index.search(query_embedding, top_k)
    return [chunks[i] for i in indices[0]]

# Step 6: Generate an answer using Cohere's Generate API
def generate_answer(query, context):
    prompt = f"Context: {context}\n\nQuestion: {query}\n\nAnswer:"
    
    headers = {
        "Authorization": f"Bearer {COHERE_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "prompt": prompt,
        "model": "command-xlarge-nightly",
        "max_tokens": 100,
        "temperature": 0.5
    }

    response = requests.post("https://api.cohere.ai/v1/generate", headers=headers, json=data)

    if response.status_code == 200:
        return response.json()['generations'][0]['text'].strip()
    else:
        raise Exception(f"Error generating answer: {response.text}")

# Step 7: Main workflow
def rag_pdf_workflow(pdf_path, query):
    pdf_text = extract_text_from_pdf(pdf_path)
    chunks = split_text_into_chunks(pdf_text)
    embeddings = create_embeddings(chunks)
    index, chunk_data = build_faiss_index(embeddings, chunks)
    relevant_chunks = retrieve_relevant_chunks(query, index, chunk_data)
    context = " ".join(relevant_chunks)
    answer = generate_answer(query, context)
    return answer

# Streamlit Application
def main():
    st.title("PDF RAG with Cohere API")
    st.write("Upload a PDF, ask a question, and get an answer!")

    # File uploader
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])
    
    if uploaded_file:
        query = st.text_input("Enter your question:")
        if query:
            try:
                # Save the uploaded PDF to a temporary file
                temp_pdf_path = f"temp_{uploaded_file.name}"
                with open(temp_pdf_path, "wb") as f:
                    f.write(uploaded_file.read())

                # Run the RAG workflow
                st.write("Processing...")
                answer = rag_pdf_workflow(temp_pdf_path, query)
                st.success(f"Answer: {answer}")
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
