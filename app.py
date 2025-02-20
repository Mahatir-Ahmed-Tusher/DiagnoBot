import gradio as gr
from langchain_huggingface import HuggingFaceEmbeddings  # Updated import
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

# Initialize LLM using ChatGroq
from langchain_groq import ChatGroq  

def initial_llm():
    llm = ChatGroq(
        temperature=0,
        groq_api_key="Replace_Your_Gloq_API_Key_Here",
        model_name="llama-3.3-70b-versatile"
    )
    return llm

def create_db():
    # Specify the exact path to the PDF in the root directory
    pdf_path = "The_GALE_ENCYCLOPEDIA_of_MEDICINE_SECOND.pdf"
    
    # Check if the PDF exists
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"🚨 PDF file not found at: {pdf_path}")

    # Load the PDF
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    
    # Split the text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(docs)
    
    # Generate embeddings using the updated HuggingFaceEmbeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    # Store data in ChromaDB
    db_path = "./chroma_db"
    vector_db = Chroma.from_documents(texts, embeddings, persist_directory=db_path)
    vector_db.persist()
    
    print("✅ ChromaDB created and medical data saved!")
    return vector_db

def setup_qachain(vector_db, llm):
    retriever = vector_db.as_retriever()
    
    # Define the prompt template
    prompt_template = """You are DiagnoBot, a medical assistant providing reliable health information:
    {context}
    User: {question}
    Chatbot: """
    
    PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    
    # Set up the QA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": PROMPT}
    )
    return qa_chain

# Load or create database
db_path = "./chroma_db"
if not os.path.exists(db_path):
    vector_db = create_db()
else:
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_db = Chroma(persist_directory=db_path, embedding_function=embeddings)

# Initialize LLM and QA chain
llm = initial_llm()
qa_chain = setup_qachain(vector_db, llm)

# Chatbot response function
def chatbot_response(query, history):
    if query.lower() == "exit":
        return "Take care! Feel free to ask anytime. Goodbye! 👋"
    response = qa_chain.invoke({"query": query})
    history.append((query, response["result"]))
    return "", history

# Gradio Interface
def launch_chatbot():
    with gr.Blocks() as demo:
        gr.Markdown("# 🏥 DiagnoBot - Your AI Medical Assistant")
        gr.Markdown("Powered by LangChain, ChromaDB, and Llama-3. Get medical insights instantly!")
        
        chatbot = gr.Chatbot()
        query_input = gr.Textbox(placeholder="Ask about symptoms, conditions, or treatments...")
        submit_button = gr.Button("Send")
        
        submit_button.click(chatbot_response, inputs=[query_input, chatbot], outputs=[query_input, chatbot])
        
        gr.Markdown("---")
        gr.Markdown("### Made By: Mahatir Ahmed Tusher")
        gr.Markdown("[GitHub](https://github.com/Mahatir-Ahmed-Tusher/EarlyMed-DiagnoBot)")
        
    demo.launch(share=True)

# Launch the chatbot
launch_chatbot()
