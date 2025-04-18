# Ask My PDFs 📚

This is a local Generative AI app powered by **Ollama**, **LangChain**, and **Streamlit** that allows you to:
- Upload **multiple PDFs**
- Ask questions across all documents
- Maintain **chat history**
- **Clear** and **download** the conversation

## 🧠 Stack
- `Ollama` (LLMs like LLaMA 3, Mistral)
- `LangChain` (RAG + vector search)
- `ChromaDB` (local vector store)
- `SentenceTransformers` (local embeddings)
- `Streamlit` (interactive UI)

## 🚀 How to Run

1. Install [Ollama](https://ollama.com) and run a model (e.g., LLaMA 3):
    ```
    ollama run llama3
    ```

2. Clone this repo and install Python dependencies:
    ```
    pip install -r requirements.txt
    ```

3. Launch the app:
    ```
    streamlit run app.py
    ```

## 🧪 Demo Notebook
See `demo_notebook.ipynb` (coming soon) for example use.

---

> Built with ❤️ by a curious data scientist.
