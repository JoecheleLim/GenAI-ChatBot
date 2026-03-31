 # <img src="logo.png" alt="Logo" width="200">
 > GenAI-ChatBot

**Glorious** is a cutting-edge, Retrieval-Augmented Generation (RAG) chatbot designed to provide expert-level Python tutoring. Built with **Streamlit** and powered by the latest **Google Gemini** models, it transforms static documentation into an interactive, conversational learning experience.

---

## 🚀 Key Features

* **Multi-Model Intelligence:** Toggle between **Gemini 3 Flash (Preview)** for instant speed, **Gemini 2.5 Flash** for balanced speed and accuracy, **Gemini 2.5 Pro** for deep logical reasoning and debugging.
* **Smart Context Retrieval (RAG):** Uses **LlamaIndex** to search and prioritise local Python guides and documentation before generating responses.
* **Modern Streaming UI:** A custom-branded interface with real-time text streaming and status updates for a seamless user experience.
* **Custom Brand Header:** Features a perfectly aligned, centred logo and title design for a professional software feel.

---

## 🛠️ Tech Stack

* **Frontend:** [Streamlit](https://streamlit.io/)
* **AI Models:** * `Gemini 3 Flash (Preview)`: For lightning-fast responses.
    * `Gemini 2.5 Pro`: For complex architectural and logic questions.
    * `Gemini 2.5 Flash`: For stable, daily assistance.
* **Data Framework:** [LlamaIndex](https://www.llamaindex.ai/) (Vector Indexing)
* **Language:** Python 3.10+

---

## 📦 Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/JoecheleLim/glorious-python-tutor.git](https://github.com/JoecheleLim/glorious-python-tutor.git)
    cd glorious-python-tutor
    ```

2.  **Environment Setup (Miniconda):**
    ```bash
    conda create -n glorious python=3.10
    conda activate glorious
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the App:**
    ```bash
    streamlit run main.py
    ```

---

## 📖 How It Works

1.  **API Integration:** Users provide their own Google Gemini API key via the secure sidebar.
2.  **Data Indexing:** The app reads files in the `/data` directory (e.g., Python syntax guides, library documentation).
3.  **Query Processing:** When a question is asked, the system retrieves relevant "facts" from the vector index.
4.  **Augmented Response:** The AI combines the retrieved facts with its internal Python knowledge to provide a highly accurate, grounded answer.

---

## 📁 Project Structure

* `main.py`: Main application loop and chat state management.
* `setup_st.py`: UI/UX design, custom CSS, and header centring logic.
* `index_functions.py`: Handles data loading and LlamaIndex vector storage.
* `helper_functions.py`: Logic for generating AI responses with streaming.
* `logo.png`: The brand assets for the application.

---

## ⚖️ License

Distributed under the MIT License. See `LICENSE` for more information.
