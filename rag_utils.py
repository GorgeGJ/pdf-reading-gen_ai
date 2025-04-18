import os
import requests
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

def load_and_split_pdfs(folder_path):
    all_docs = []
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(folder_path, file))
            docs = loader.load()
            chunks = splitter.split_documents(docs)
            all_docs.extend(chunks)
    return all_docs

def embed_documents(docs, persist_dir="chroma_db"):
    embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectordb = Chroma.from_documents(docs, embedding, persist_directory=persist_dir)
    vectordb.persist()
    return vectordb

def query_ollama(context, query, model="llama3"):
    prompt = f"Use the following context to answer the question:\n{context}\n\nQ: {query}\nA:"
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": model, "prompt": prompt, \
              "temperature": 0.5,  # Lower = more deterministic, default 0.7
              "stream": False}
    )
    return response.json()["response"]
