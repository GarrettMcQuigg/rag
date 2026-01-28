"""
Document ingestion pipeline.
Handles loading documents from various sources and chunking them for embedding.
"""

import uuid
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.config import Config
from src.vectorstore import upsert_documents


def create_text_splitter() -> RecursiveCharacterTextSplitter:
    """Create a text splitter with configured chunk size and overlap."""
    return RecursiveCharacterTextSplitter(
        chunk_size=Config.CHUNK_SIZE,
        chunk_overlap=Config.CHUNK_OVERLAP,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )


def chunk_text(text: str, metadata: dict = None) -> list[dict]:
    """
    Split text into chunks and prepare for upserting.
    
    Args:
        text: The full text to chunk.
        metadata: Optional metadata to attach to each chunk.
    
    Returns:
        List of document dicts ready for upserting.
    """
    splitter = create_text_splitter()
    chunks = splitter.split_text(text)
    
    documents = []
    for i, chunk in enumerate(chunks):
        doc = {
            "id": str(uuid.uuid4()),
            "text": chunk,
            "metadata": {
                "chunk_index": i,
                **(metadata or {})
            }
        }
        documents.append(doc)
    
    return documents


def load_text_file(file_path: str) -> str:
    """Load text content from a file."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    return path.read_text(encoding="utf-8")


def ingest_text_file(file_path: str) -> dict:
    """
    Load a text file, chunk it, and upsert to Pinecone.
    
    Args:
        file_path: Path to the text file.
    
    Returns:
        Upsert response from Pinecone.
    """
    text = load_text_file(file_path)
    metadata = {"source": str(file_path)}
    documents = chunk_text(text, metadata)
    
    print(f"Ingesting {len(documents)} chunks from {file_path}")
    return upsert_documents(documents)


def ingest_text(text: str, source_name: str = "direct_input") -> dict:
    """
    Chunk raw text and upsert to Pinecone.
    
    Args:
        text: The text content to ingest.
        source_name: A name to identify the source in metadata.
    
    Returns:
        Upsert response from Pinecone.
    """
    metadata = {"source": source_name}
    documents = chunk_text(text, metadata)
    
    print(f"Ingesting {len(documents)} chunks from {source_name}")
    return upsert_documents(documents)


def ingest_directory(directory_path: str, extensions: list[str] = None) -> list[dict]:
    """
    Ingest all text files from a directory.
    
    Args:
        directory_path: Path to the directory.
        extensions: List of file extensions to include (e.g., [".txt", ".md"]).
                   Defaults to [".txt", ".md"].
    
    Returns:
        List of upsert responses.
    """
    if extensions is None:
        extensions = [".txt", ".md"]
    
    path = Path(directory_path)
    if not path.exists():
        raise FileNotFoundError(f"Directory not found: {directory_path}")
    
    responses = []
    for ext in extensions:
        for file_path in path.glob(f"*{ext}"):
            response = ingest_text_file(str(file_path))
            responses.append(response)
    
    return responses
