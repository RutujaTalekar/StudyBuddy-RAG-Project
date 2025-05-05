#!/bin/bash

echo "📦 Starting StudyBuddy setup..."

# Check if PDF exists
if [ ! -f "data/Alex-Xu-SysDesignHandbook.pdf" ]; then
    echo "❌ Book PDF not found at data/Alex-Xu-SysDesignHandbook.pdf"
    echo "Please mount it correctly using: -v $(pwd)/data:/app/data"
    exit 1
fi

# Extract text if JSON doesn't exist
if [ ! -f "data/book_pages.json" ]; then
    echo "📖 Extracting text from PDF..."
    python3 src/extract_text.py
fi

# Build vectorstore if not present
if [ ! -d "alexxu_db" ]; then
    echo "📚 Building vector store..."
    python3 src/build_vectorstore.py
fi

# Start chatbot
echo "🤖 Launching chatbot..."
python3 src/rag_query.py
