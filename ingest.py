import os
from dotenv import load_dotenv
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Pinecone as LangchainPinecone
from pinecone import Pinecone, ServerlessSpec

load_dotenv()

# Load and chunk PDF(s)
loader = PyPDFLoader("data/your_textbook.pdf")  # or loop over multiple
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(documents)

# Embeddings
embedding_model = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")

# Pinecone setup
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index_name = "ai-tutor-index"

if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region=os.getenv("PINECONE_ENVIRONMENT"))
    )

index = pc.Index(index_name)
vectorstore = LangchainPinecone.from_documents(chunks, embedding_model, index_name=index_name)
print("Knowledge base indexed!")
