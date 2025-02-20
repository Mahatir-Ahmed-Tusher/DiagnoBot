![logo](https://github.com/user-attachments/assets/1dc527d3-6f76-4efa-bfbe-126816baba69)


# EarlyMed DiagnoBot
DiagnoBot is an innovative, AI-powered medical assistant designed to provide reliable, context-aware health information based on a comprehensive medical reference. Developed as a side project of EarlyMed, DiagnoBot leverages state-of-the-art natural language processing and retrieval techniques to answer your medical queries with precision and empathy.

---

## Table of Contents

- [Overview](#overview)
- [How It Works](#how-it-works)
  - [Document Ingestion and Preprocessing](#document-ingestion-and-preprocessing)
  - [Embedding Generation and Vector Storage](#embedding-generation-and-vector-storage)
  - [Query Processing and Response Generation](#query-processing-and-response-generation)
  - [User Interface](#user-interface)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [Acknowledgements](#acknowledgements)
- [License](#license)

---

## Overview

DiagnoBot transforms a static, authoritative medical reference into a dynamic, interactive tool. At its core, DiagnoBot uses *The\_GALE\_ENCYCLOPEDIA\_of\_MEDICINE\_SECOND.pdf* as its knowledge base, processing and storing information from this comprehensive document so that it can retrieve relevant details in response to user queries. Whether you’re asking about symptoms, conditions, or treatments, DiagnoBot is built to provide insightful and reliable answers.

---

## How It Works

### Document Ingestion and Preprocessing

- **PDF Source:**\
  DiagnoBot uses the renowned *The\_GALE\_ENCYCLOPEDIA\_of\_MEDICINE\_SECOND.pdf*, placed in the root directory of the repository. This medical encyclopedia is a robust source of information that covers a wide array of health topics.

- **Loading the Document:**\
  The PDF is ingested using `PyPDFLoader` from the `langchain_community.document_loaders` package. This ensures that the textual content is extracted accurately from every page of the document.

- **Splitting the Text:**\
  To facilitate efficient retrieval, the extracted text is segmented into manageable chunks using the `RecursiveCharacterTextSplitter`. Each chunk is 500 characters long with a 50-character overlap. This approach helps in capturing the context more effectively and improves the accuracy of information retrieval.

### Embedding Generation and Vector Storage

- **Embedding Generation:**\
  Each text chunk is converted into a high-dimensional vector using the `HuggingFaceEmbeddings` class from the `langchain_huggingface` package. The "sentence-transformers/all-MiniLM-L6-v2" model powers these embeddings, ensuring that the semantic meaning of the text is captured effectively.

- **Vector Database (ChromaDB):**\
  These embeddings are stored in ChromaDB, a robust vector database that supports fast similarity searches. This allows DiagnoBot to quickly retrieve the most relevant sections of text from the vast encyclopedia based on the user's query.

### Query Processing and Response Generation

- **Retrieval-Based QA Chain:**\
  When a user asks a question, DiagnoBot uses a retrieval-based question-answering (QA) chain. The system first embeds the query and then searches ChromaDB to retrieve the most relevant text segments.

- **Custom Prompting:**\
  A carefully crafted prompt template instructs the language model to act as a knowledgeable and empathetic medical assistant. The retrieved context and the query are passed to the LLM, which generates a response that blends factual accuracy with clear, empathetic language.

- **LLM Powered by ChatGroq:**\
  DiagnoBot uses an LLM provided via the ChatGroq API, which accesses the powerful Llama‑3.3‑70B model. With temperature set to 0, the model provides deterministic, reliable responses ideal for medical advice.

### User Interface

- **Gradio-Powered Web Interface:**\
  The entire system is integrated into an intuitive Gradio interface. Users interact with DiagnoBot through a sleek chat window, where they can enter their queries and receive immediate responses. This makes the assistant highly accessible, whether for personal health inquiries or educational purposes.

---

## Project Structure

- **DiagnoBot.ipynb:**\
  A Jupyter Notebook detailing experiments, code walkthroughs, and testing procedures that led to the development of DiagnoBot.

- **app.py:**\
  The main application file that sets up the Gradio web interface, initializes the document processing pipeline, and launches the interactive chatbot.

- **The\_GALE\_ENCYCLOPEDIA\_of\_MEDICINE\_SECOND.pdf:**\
  The comprehensive medical reference that serves as the foundational knowledge base for DiagnoBot. This file must reside in the root directory of the repository.

- **requirements.txt:**\
  Lists all the required Python packages to ensure that the environment is set up correctly both locally and on Hugging Face Spaces.

---

## Installation

### Local Setup

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/Mahatir-Ahmed-Tusher/DiagnoBot.git
   cd DiagnoBot
   ```

2. **Set Up a Virtual Environment (Recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application:**

   ```bash
   python app.py
   ```

   This command will launch the Gradio interface locally, allowing you to interact with DiagnoBot.

---

## Usage

Once the application is running:

- **Input:** Type your medical queries into the chat box (e.g., "What are the symptoms of diabetes?" or "Tell me about hypertension treatments").
- **Output:** DiagnoBot will process your query, retrieve relevant information from *The\_GALE\_ENCYCLOPEDIA\_of\_MEDICINE\_SECOND.pdf*, and generate an insightful response.
- **Exit:** Simply type "exit" to end the session.

---

## Deployment

DiagnoBot is deployed on Hugging Face Spaces for easy public access. Visit the live version here:

[https://huggingface.co/spaces/MahatirTusher/DiagnoBot-V2](https://huggingface.co/spaces/MahatirTusher/DiagnoBot-V2)

---

## Acknowledgements

- **Ashmit Jain:**\
  Special thanks to Ashmit Jain for inspiring the idea behind this project. His work and vision provided the spark that led to the creation of DiagnoBot.

- **The GALE ENCYCLOPEDIA of MEDICINE:**\
  This comprehensive medical reference is the cornerstone of DiagnoBot’s knowledge base. Its depth and accuracy have been instrumental in building a reliable assistant.

- **EarlyMed:**\
  The project is a proud side initiative of EarlyMed, aiming to enhance access to medical information through cutting-edge AI technology.

---

## License

DiagnoBot is released under the [MIT License](LICENSE). Feel free to use, modify, and distribute this project as per the license terms.





DiagnoBot is a testament to the power of modern AI in transforming traditional resources into dynamic, interactive assistants. We hope it serves as a valuable tool for anyone seeking medical insights and encourages further innovation in AI-driven healthcare solutions.

A side project of,

![logo](https://github.com/user-attachments/assets/e3715b9d-508b-4715-9838-4254f12402a2)

