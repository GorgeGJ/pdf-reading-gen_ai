import os
import streamlit as st
from rag_utils import load_and_split_pdfs, embed_documents, query_ollama
from langchain.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from streamlit_chat import message
from streamlit_extras.row import row
from streamlit_extras.stylable_container import stylable_container

PDF_DIR = "pdfs"
DB_DIR = "chroma_db"

st.set_page_config(page_title="Ask My PDFs", layout="wide")
st.title("📚 Ask My PDFs")

# Sidebar options
st.sidebar.title("Settings")
selected_model = st.sidebar.selectbox("Choose model", ["llama3", "mistral", "gemma"])

# Session state for chat
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Upload PDFs
with stylable_container(key="upload-box", css_styles="padding: 1rem; border: 1px solid #ccc; border-radius: 10px;"):
    uploaded_files = st.file_uploader("📎 Upload PDF(s)", type="pdf", accept_multiple_files=True)
    if uploaded_files:
        os.makedirs(PDF_DIR, exist_ok=True)
        for file in uploaded_files:
            with open(os.path.join(PDF_DIR, file.name), "wb") as f:
                f.write(file.read())
        st.success("Uploaded successfully!")

# Embed docs
if st.button("📌 Embed All PDFs"):
    with st.spinner("Processing..."):
        docs = load_and_split_pdfs(PDF_DIR)
        vectordb = embed_documents(docs, persist_dir=DB_DIR)
        st.success("Embedding complete.")

# Chat input
query = st.chat_input("Ask a question about your PDFs:")
if query:
    embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectordb = Chroma(persist_directory=DB_DIR, embedding_function=embedding)
    retriever = vectordb.as_retriever()
    relevant_docs = retriever.invoke(query)
    context = "\n".join([doc.page_content for doc in relevant_docs[:3]])

    # Add chat history to context
    history_context = "\n".join([f"Q: {q}\nA: {a}" for q, a in st.session_state.chat_history])
    full_context = history_context + "\n" + context if history_context else context

    # Query the model
    answer = query_ollama(full_context, query, model=selected_model)
    st.session_state.chat_history.append((query, answer))

# Display chat bubbles
for i, (q, a) in enumerate(st.session_state.chat_history):
    message(q, is_user=True, key=f"user-{i}")
    message(a, key=f"bot-{i}")

# Chat tools
col1, col2 = st.columns(2)
with col1:
    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.experimental_rerun()

with col2:
    chat_text = "\n\n".join([f"Q: {q}\nA: {a}" for q, a in st.session_state.chat_history])
    st.download_button("📄 Download Chat", chat_text, file_name="chat_history.txt")
