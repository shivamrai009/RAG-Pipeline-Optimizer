import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_chroma import Chroma
# --- FIX: Use langchain_core for prompts ---
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

# 1. Flexible RAG Pipeline Builder
def build_rag_pipeline(docs, chunk_size, chunk_overlap):
    # A. Splitting
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    splits = text_splitter.split_documents(docs)

    # B. Embedding (Runs locally on CPU - FREE)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)
    retriever = vectorstore.as_retriever()

    # C. Generation (Using Llama-3 via Groq - FREE tier)
    llm = ChatGroq(model_name="llama-3.1-8b-instant", temperature=0)
    
    template = """Answer the question based only on the following context:
    {context}
    
    Question: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)

    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain, retriever

# 2. The Experiment Runner
async def run_experiments(file_path: str, question: str):
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    
    results = []
    
    # We test 3 different strategies
    strategies = [
        {"name": "Quick Glance", "chunk": 512, "overlap": 50},
        {"name": "Deep Dive", "chunk": 1024, "overlap": 200},
        {"name": "Precise Snippet", "chunk": 256, "overlap": 20}
    ]
    
    print(f"--- Starting Experiments for: {question} ---")
    
    for strategy in strategies:
        print(f"Running strategy: {strategy['name']}...")
        chain, retriever = build_rag_pipeline(docs, strategy["chunk"], strategy["overlap"])
        
        answer = chain.invoke(question)
        
        # Get Context for the evaluator to see
        retrieved_docs = retriever.invoke(question)
        context_text = "\n".join([doc.page_content for doc in retrieved_docs])
        
        results.append({
            "strategy": strategy["name"],
            "chunk_size": strategy["chunk"],
            "answer": answer,
            "context": context_text
        })
        
    return results