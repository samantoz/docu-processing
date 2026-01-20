# docu-processing - Document Processing and AI Chat System

A comprehensive document processing pipeline built with Docling that converts PDFs to markdown, chunks documents with LangChain, generates embeddings, stores them in ChromaDB, and provides an AI-powered chat interface for document Q&A.

## Table of contents

- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
      - For Ollama setup, see [Ollama Setup Guide](ollama.md)
  - [Executing the environment](#executing-the-environment)
  - [Environment Setup](#environment-setup)
- [Usage](#usage)
  - [1. Convert PDFs to Markdown](#1-convert-pdfs-to-markdown)
  - [2. Chunk Documents](#2-chunk-documents)
  - [3. Generate and Store Embeddings](#3-generate-and-store-embeddings)
  - [4. Chat with Your Documents](#4-chat-with-your-documents)
- [Configuration Options](#configuration-options)
  - [Embedding Providers](#embedding-providers)
    - [OpenAI (Default)](#openai-default)
    - [Ollama (Local)](#ollama-local)
  - [Chunking Strategies](#chunking-strategies)
  - [ChromaDB Configuration](#chromadb-configuration)
- [Project Structure](#project-structure)
- [Development](#development)
  - [Testing](#testing)
  - [Code Quality](#code-quality)
- [Contributing](#contributing)
- [License](#license)
- [Troubleshooting](#troubleshooting)
  - [Common Issues](#common-issues)
  - [Support](#support)
- [Dependencies](#dependencies)
- [Version](#version)
- [Requirements](#requirements)
- [More Research Topics](#Advanced-Topics)
---

## Features

- **PDF to Markdown Conversion:** Extract and convert PDF documents to structured markdown format.
- **Intelligent Document Chunking:** Use LangChain's RecursiveCharacterTextSplitter for semantic chunking.
- **Vector Embeddings:** Generate embeddings using OpenAI or Ollama models.
- **Vector Storage:** Persistent storage with ChromaDB for efficient similarity search.
- **AI Chat Interface:** Interactive chat with your documents using Retrieval-Augmented Generation (RAG).
- **Multiple Embedding Providers:** Support for OpenAI, Azure OpenAI, and Ollama embedding models.

---

## Architecture

The system follows a modular pipeline architecture:

1. **Document Conversion:** PDF files converted to markdown using Docling.
2. **Text Chunking:** Markdown content split into semantic chunks with LangChain.
3. **Embedding Generation:** Text chunks converted to vector embeddings.
4. **Vector Storage:** Embeddings stored in ChromaDB for efficient retrieval.
5. **RAG Chat:** AI-powered Q&A using context from retrieved document chunks.

---

## Installation

### Prerequisites

- Python 3.9+ (< 3.13)
- OpenAI API key (for OpenAI embeddings/chat), Azure OpenAI credentials, or Ollama (for local models)
- Tesseract OCR (required for PDF processing): `sudo apt-get install tesseract-ocr` (Linux) or `brew install tesseract` (macOS)
- Google Drive API credentials (for downloading files from Google Drive)
- For Ollama setup, see [Ollama Setup Guide](ollama.md)

### Executing the environment
```bash
# Activate virtual environment
source .venv/bin/activate
 
# List all installed packages
uv pip list

# Check for a specific package (requests)
uv pip show requests

```
### Environment Setup

```bash
# Clone the repository
git clone <repository-url>
cd personal-finance-analysis

# Install dependencies with uv
uv sync

# For development with additional tools
uv sync --extra dev

# For all optional dependencies  
uv sync --all-extras
```

Set up environment variables by creating a `.env` file:

```env
# Embedding Model Configuration
EMBEDDING_PROVIDER=openai  # Options: 'openai', 'azure_openai', 'ollama'
OPENAI_EMBEDDING_MODEL=text-embedding-ada-002
OLLAMA_EMBEDDING_MODEL=jina/jina-embeddings-v2-base-en
OLLAMA_BASE_URL=http://localhost:11434

# Chat Provider Configuration
# Options: 'openai', 'azure_openai', 'ollama'
CHAT_PROVIDER=openai

# OpenAI Chat Configuration (when CHAT_PROVIDER=openai)
OPENAI_API_KEY=your_openai_api_key
OPENAI_CHAT_MODEL=gpt-4o
MAX_TOKENS=500


# Ollama Chat Configuration (when CHAT_PROVIDER=ollama)
OLLAMA_CHAT_MODEL=qwen3:0.6b
OLLAMA_BASE_URL=http://localhost:11434

# ChromaDB Configuration
CHROMA_DB_PATH=./chroma_db
CHROMA_COLLECTION_NAME=documents
```

### Google Drive Setup

To download files from Google Drive, you need to set up Google Drive API credentials:

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project or select an existing one.
3. Enable the Google Drive API.
4. Create OAuth 2.0 credentials (download the `credentials.json` file).
5. Place `credentials.json` in the project root directory.

The script will handle authentication and create a `token.pickle` file for future use.

---

## Usage

### 0. Download Files from Google Drive

Download files from Google Drive into subfolders under `data/docs/`.

```bash
# Download a file by ID into a specific subfolder
uv run scripts/download_from_drive.py <file_id> <subfolder_name>

# Example
uv run scripts/download_from_drive.py 1abc123def456 subfolder_name

# With custom base path and credentials
uv run scripts/download_from_drive.py <file_id> <subfolder_name> --base-path data/docs --credentials credentials.json --token token.pickle
```

**Note:** The first run will open a browser for Google authentication. Subsequent runs will use the saved token.

### 1. Convert PDFs to Markdown

```bash
# Convert all PDFs from docs/ folder to markdown in docs_md/
uv run scripts/pdf_to_markdown.py --input data/docs/ --output data/docs_md/

# Convert single PDF file
uv run scripts/pdf_to_markdown.py --input data/docs/{document.pdf} --output data/docs_md/{document.md}
```

### 2. Chunk Documents

```bash
# Chunk all markdown files with default settings (1000 chars, 200 overlap)
uv run scripts/chunk_documents.py --input data/docs_md/ --output chunks/ --chunk-size 1000 --overlap 200

# Custom chunking parameters
uv run scripts/chunk_documents.py --input data/docs_md/ --output chunks/ --chunk-size 500 --overlap 100 --chunk-method recursive
```

### 3. Generate and Store Embeddings

```bash
# Initialize ChromaDB collection (run once)
uv run scripts/init_chroma.py --db-path chroma_db/ --collection-name documents

# Generate embeddings using OpenAI (default)
uv run scripts/generate_embeddings.py --input chunks/ --db-path chroma_db/ --provider openai --model text-embedding-ada-002

# Generate embeddings using Azure OpenAI
uv run scripts/generate_embeddings.py --input chunks/ --db-path chroma_db/ --provider azure_openai --model text-embedding-3-small

# Generate embeddings using Ollama
uv run scripts/generate_embeddings.py --input chunks/ --db-path chroma_db/ --provider ollama --model jina/jina-embeddings-v2-base-en

# Use environment variables (set EMBEDDING_PROVIDER in .env)
uv run scripts/generate_embeddings.py --input chunks/ --db-path chroma_db/
```

### 4. Chat with Your Documents

```bash
# Interactive chat mode with OpenAI
uv run scripts/chat_with_docs.py --db-path chroma_db/ --model gpt-4

# Interactive chat mode with Azure OpenAI
uv run scripts/chat_with_docs.py --db-path chroma_db/ --model gpt-4.1-mini

# Query embeddings directly with OpenAI
uv run scripts/query_embeddings.py --query "your question here" --db-path chroma_db/ --model gpt-4 --embedding-provider openai --chat-provider openai

# Query embeddings directly with Azure OpenAI
uv run scripts/query_embeddings.py --query "your question here" --db-path chroma_db/ --model gpt-4.1-mini --embedding-provider azure_openai --chat-provider azure_openai
```

---

## Configuration Options

### Embedding Providers

**OpenAI (Default):**
- Model: `text-embedding-ada-002`
- Requires: `OPENAI_API_KEY` environment variable
- High quality embeddings with API costs

**Ollama (Local):**
- Model: `jina/jina-embeddings-v2-base-en` (configurable)
- Requires: Local Ollama installation
- Free local processing, requires more setup

### Chunking Strategies

- **Recursive Character Text Splitter:** Smart splitting that preserves semantic boundaries
- **Chunk Size:** Default 1000 characters (adjustable)
- **Overlap:** Default 200 characters for context preservation

### ChromaDB Configuration

- **Persistent Storage:** Vector embeddings stored locally in `chroma_db/`
- **Collection Name:** Default "documents" (configurable)
- **Metadata:** Includes source file and chunk information

---

## Project Structure

```
docu-processing/
  scripts/                    # Main processing scripts
    pdf_to_markdown.py        # PDF conversion
    chunk_documents.py        # Document chunking
    generate_embeddings.py    # Embedding generation
    query_embeddings.py       # Direct querying
    chat_with_docs.py         # Interactive chat
    init_chroma.py            # ChromaDB initialization
    embedding_models.py       # Model configuration
  docling/                    # Core Docling library
  data/                       # Input documents
  docs_md/                    # Converted markdown files
  chunks/                     # Chunked text files
  chroma_db/                  # ChromaDB vector storage
  .env                        # Environment configuration
  pyproject.toml              # Project dependencies
```

---

## Development

### Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_document_converter.py

# Run tests with coverage
pytest --cov=docling
```

### Code Quality

```bash
# Format code
black docling/
isort docling/

# Lint code
flake8 docling/
mypy docling/
```

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite and linting
6. Submit a pull request

---

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## Troubleshooting

### Common Issues

- **ChromaDB Errors:** Ensure ChromaDB is properly initialized with `init_chroma.py`
- **OpenAI API Errors:** Verify your API key is set in the `.env` file
- **Ollama Connection Issues:** Check that Ollama is running locally on the specified port
- **Memory Issues:** For large documents, reduce chunk size or process in smaller batches

### Support

For issues and questions:
1. Check the troubleshooting section above
2. Review the script help messages with `--help`
3. Open an issue on the project repository

---

## Dependencies

- **chromadb:** Vector database for embedding storage
- **langchain:** Document processing and chunking
- **langchain-openai:** OpenAI integration for LangChain
- **openai:** OpenAI API client
- **python-dotenv:** Environment variable management
- **filetype:** File type detection

---

## Version

Current version: **0.1.0**

---

## Requirements

- Python: >= 3.9, < 3.13
- See `pyproject.toml` for complete dependency list

## Advanced-Topics

- How AI moves from stateless models → autonomous agents

- The real meaning of context engineering, memory, and sessions

- Why MCP is becoming the USB-C of AI interoperability

- How to avoid demo-ware and ship production-grade agents

- The new discipline of Agent Quality & Evaluation Engineering
