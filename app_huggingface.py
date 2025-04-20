
import os
import streamlit as st
from rag_utils import load_and_split_pdfs, embed_documents, query_huggingface
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from streamlit_chat import message
from streamlit_extras.row import row
from streamlit_extras.stylable_container import stylable_container

PDF_DIR = "pdfs"
DB_DIR = "chroma_db"

st.set_page_config(page_title="Ask My PDFs", layout="wide")
st.title("📚 Ask My PDFs")

# Sidebar options
st.sidebar.title("Settings")
selected_model = st.sidebar.selectbox("Choose model", ["distilbert-base-uncased-distilled-squad", "deepset/roberta-base-squad2"])
api_token = st.sidebar.text_input("🔐 Hugging Face API Token", type="password")

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

# Process PDFs
vectordb = None
if os.path.exists(PDF_DIR):
    docs = load_and_split_pdfs(PDF_DIR)
    vectordb = embed_documents(docs, persist_dir=DB_DIR)
    retriever = vectordb.as_retriever()

# Chat UI
query = st.text_input("Ask a question about your PDFs:")
if query and vectordb:
    context_docs = retriever.get_relevant_documents(query)
    context_text = " ".join([doc.page_content for doc in context_docs])
    if api_token:
        try:
            answer = query_huggingface(context_text, query, api_token, model=selected_model)
        except Exception as e:
            answer = f"⚠️ Error: {e}"
    else:
        answer = "⚠️ Please enter your Hugging Face API token in the sidebar."

    st.session_state.chat_history.append(("user", query))
    st.session_state.chat_history.append(("ai", answer))

# Display chat history
for role, message_text in st.session_state.chat_history:
    message(message_text, is_user=(role == "user"))
