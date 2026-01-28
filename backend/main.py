"""
RAG Project - Main Entry Point

This script demonstrates the basic RAG functionality:
1. Ingest documents from the data/ folder
2. Query the vector store
3. Retrieve relevant context

Usage:
    python main.py ingest     # Load documents into Pinecone
    python main.py query      # Interactive query mode
    python main.py stats      # Show index statistics
    python main.py clear      # Clear all documents (use with caution!)
"""

import sys
from src.ingest import ingest_directory
from src.generator import generate_response
from src.retriever import search_and_print, retrieve_as_context
from src.vectorstore import get_index_stats, delete_all_documents


def ingest_data():
    """Ingest all documents from the data directory."""
    print("📥 Ingesting documents from data/ folder...")
    try:
        responses = ingest_directory("data", extensions=[".txt", ".md"])
        print(f"✅ Successfully ingested {len(responses)} file(s)")
    except Exception as e:
        print(f"❌ Error during ingestion: {e}")


def interactive_query():
    """Run interactive query mode."""
    print("🔍 Interactive Query Mode")
    print("Type 'quit' or 'exit' to stop\n")
    
    while True:
        query = input("Enter your query: ").strip()
        
        if query.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break
        
        if not query:
            continue
        
        search_and_print(query, top_k=3)
        print()


def show_stats():
    """Display index statistics."""
    print("📊 Index Statistics")
    print("=" * 30)
    stats = get_index_stats()
    print(f"Total vectors: {stats.total_vector_count}")
    print(f"Namespaces: {list(stats.namespaces.keys()) if stats.namespaces else ['default']}")


def clear_index():
    """Clear all documents from the index."""
    confirm = input("⚠️  This will delete ALL documents. Type 'yes' to confirm: ")
    if confirm.lower() == "yes":
        delete_all_documents()
        print("🗑️  All documents deleted.")
    else:
        print("Cancelled.")


def ask_question():
    """Full RAG: retrieve context and generate answer."""
    print("💬 RAG Question Answering")
    print("Type 'quit' or 'exit' to stop\n")
    
    while True:
        query = input("Ask a question: ").strip()
        
        if query.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break
        
        if not query:
            continue
        
        print("\n🔍 Retrieving context...")
        context = retrieve_as_context(query, top_k=3)
        
        print("🤖 Generating answer...\n")
        answer = generate_response(query, context)
        
        print(f"{answer}\n")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    
    command = sys.argv[1].lower()
    
    if command == "ingest":
        ingest_data()
    elif command == "query":
        interactive_query()
    elif command == "ask":
        ask_question()
    elif command == "stats":
        show_stats()
    elif command == "clear":
        clear_index()
    else:
        print(f"Unknown command: {command}")
        print(__doc__)


if __name__ == "__main__":
    main()
