import os

import fitz  # PyMuPDF
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone, ServerlessSpec

load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    return "\n".join(page.get_text() for page in doc)


def upload_pdf():
    pdf_path = "Profile.pdf"
    resume_text = extract_text_from_pdf(pdf_path)
    embeddings = OpenAIEmbeddings()
    vector = embeddings.embed_query(resume_text)
    pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))
    index_name = "resume-index"
    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=1536,
            metric="euclidean",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )
    index = pc.Index(index_name)
    index.upsert([("resume-001", vector, {"text": resume_text})])

    print("✅ Resume vector uploaded successfully.")

def upload_md():
    md_path = "TimeTrackingDocumentation.md"  # 🔄 Replace with your .md file
    if not os.path.exists(md_path):
        raise FileNotFoundError(f"File not found: {md_path}")

    # Read Markdown file content
    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    # Generate embedding
    embeddings = OpenAIEmbeddings()
    vector = embeddings.embed_query(md_text)

    # Initialize Pinecone
    pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))
    index_name = "timetracking-index"

    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=1536,  # OpenAI Embeddings dimension
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )

    index = pc.Index(index_name)

    # Upsert into Pinecone
    index.upsert([("timetracking-001", vector, {"filename": md_path, "text": md_text})])

    print("✅ Markdown file vector uploaded successfully.")


if __name__ == "__main__":
    upload_md()
