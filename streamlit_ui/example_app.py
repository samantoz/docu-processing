"""Example Streamlit application using the UI framework - Document Chat Interface"""

# Ensure project root is on `sys.path` so absolute imports like
# `from streamlit_ui.core.app import ...` work when this file is executed
# directly by `streamlit run` (which can change the import context).
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st
from streamlit_ui.core.app import StreamlitApp
from streamlit_ui.core.page import Page
from streamlit_ui.core.config import AppConfig
from streamlit_ui.components import (
    render_info_box,
    render_success_box,
    render_error_box,
    FormBuilder
)
from streamlit_ui.utils.state import StateManager
from typing import Optional
import os


class HomePage(Page):
    """Home page of the application"""
    
    def __init__(self):
        super().__init__(
            name="Home",
            icon="🏠",
            description="Welcome to the Document Processing Chat System"
        )
    
    def render(self) -> None:
        self.render_header()
        
        st.markdown("""
        ### About This Application
        
        This is a powerful document processing and Q&A system that allows you to:
        
        - 📄 **Process Documents**: Convert PDFs to markdown and chunk them intelligently
        - 🧠 **Generate Embeddings**: Create vector embeddings for semantic search
        - 💬 **Chat with Documents**: Ask questions about your documents using AI
        - 🔍 **Semantic Search**: Find relevant information quickly
        
        ### Getting Started
        
        1. Navigate to the **Chat** page to ask questions
        2. Use the **Settings** page to configure embedding providers
        3. Check the **Logs** page to monitor processing activities
        
        ### Key Features
        
        - Multiple embedding providers (OpenAI, Ollama)
        - Persistent vector database (ChromaDB)
        - Interactive chat interface
        - Real-time processing logs
        """)
        
        # Statistics section
        st.subheader("📊 Quick Stats")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Embeddings", "0", "+0")
        with col2:
            st.metric("Documents", "0", "+0")
        with col3:
            st.metric("Chat Messages", "0", "+0")


class ChatPage(Page):
    """Chat interface page"""
    
    def __init__(self):
        super().__init__(
            name="Chat",
            icon="💬",
            description="Ask questions about your documents"
        )
        self.state_manager = StateManager("chat_page")
    
    def render(self) -> None:
        self.render_header()
        
        # Chat interface
        st.subheader("Ask Your Documents")
        
        # Display chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("What would you like to know?"):
            # Add user message to history
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Simulate AI response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    # This would be replaced with actual RAG implementation
                    response = f"Thank you for your question: '{prompt}'. In a real implementation, this would query the document embeddings and provide a relevant answer."
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Clear history button
        if st.button("Clear Chat History"):
            st.session_state.messages = []
            st.rerun()


class SettingsPage(Page):
    """Settings and configuration page"""
    
    def __init__(self):
        super().__init__(
            name="Settings",
            icon="⚙️",
            description="Configure application settings"
        )
    
    def render(self) -> None:
        self.render_header()
        
        st.subheader("Embedding Configuration")
        
        # Embedding provider selection
        provider = st.selectbox(
            "Select Embedding Provider",
            ["OpenAI", "Ollama", "Azure OpenAI"],
            key="embedding_provider"
        )
        
        if provider == "OpenAI":
            st.write("**OpenAI Configuration**")
            api_key = st.text_input(
                "OpenAI API Key",
                type="password",
                key="openai_api_key"
            )
            model = st.selectbox(
                "Embedding Model",
                ["text-embedding-ada-002", "text-embedding-3-small", "text-embedding-3-large"],
                key="openai_model"
            )
        
        elif provider == "Ollama":
            st.write("**Ollama Configuration**")
            base_url = st.text_input(
                "Ollama Base URL",
                value="http://localhost:11434",
                key="ollama_base_url"
            )
            model = st.text_input(
                "Embedding Model",
                value="jina/jina-embeddings-v2-base-en",
                key="ollama_model"
            )
        
        elif provider == "Azure OpenAI":
            st.write("**Azure OpenAI Configuration**")
            endpoint = st.text_input(
                "Azure OpenAI Endpoint",
                key="azure_endpoint"
            )
            api_key = st.text_input(
                "Azure API Key",
                type="password",
                key="azure_api_key"
            )
            api_version = st.text_input(
                "API Version",
                value="2023-05-15",
                key="azure_api_version"
            )
        
        st.divider()
        
        st.subheader("ChromaDB Configuration")
        db_path = st.text_input(
            "Database Path",
            value="./chroma_db",
            key="chroma_db_path"
        )
        
        collection_name = st.text_input(
            "Collection Name",
            value="documents",
            key="chroma_collection"
        )
        
        st.divider()
        
        # Save button
        if st.button("Save Settings", use_container_width=True):
            render_success_box("Settings saved successfully!")


class DocumentPage(Page):
    """Document processing page"""
    
    def __init__(self):
        super().__init__(
            name="Documents",
            icon="📚",
            description="Process and manage your documents"
        )
    
    def render(self) -> None:
        self.render_header()
        
        st.subheader("Upload and Process Documents")
        
        # File upload
        uploaded_files = st.file_uploader(
            "Upload PDF documents",
            type=["pdf"],
            accept_multiple_files=True,
            key="document_upload"
        )
        
        if uploaded_files:
            st.write(f"**{len(uploaded_files)} file(s) selected**")
            
            for file in uploaded_files:
                st.write(f"- {file.name}")
        
        st.divider()
        
        # Processing options
        st.subheader("Processing Options")
        
        col1, col2 = st.columns(2)
        
        with col1:
            chunk_size = st.slider(
                "Chunk Size (characters)",
                min_value=100,
                max_value=5000,
                value=1000,
                step=100,
                key="chunk_size"
            )
        
        with col2:
            overlap = st.slider(
                "Chunk Overlap",
                min_value=0,
                max_value=500,
                value=200,
                step=50,
                key="chunk_overlap"
            )
        
        # Process button
        if st.button("Process Documents", use_container_width=True):
            if uploaded_files:
                with st.spinner("Processing documents..."):
                    st.success(f"Successfully processed {len(uploaded_files)} document(s)")
            else:
                render_error_box("Please upload at least one document")


class LogsPage(Page):
    """Logs and monitoring page"""
    
    def __init__(self):
        super().__init__(
            name="Logs",
            icon="📋",
            description="View application logs and monitoring"
        )
    
    def render(self) -> None:
        self.render_header()
        
        # Log type selection
        log_type = st.radio(
            "Select Log Type",
            ["Process Logs", "Error Logs", "All Logs"],
            horizontal=True,
            key="log_type"
        )
        
        st.divider()
        
        # Sample logs display
        st.subheader("Recent Logs")
        
        sample_logs = [
            "2025-11-14 10:30:45 - INFO - Application started",
            "2025-11-14 10:31:12 - INFO - Document uploaded: sample.pdf",
            "2025-11-14 10:31:45 - INFO - Processing completed successfully",
            "2025-11-14 10:32:10 - INFO - Embeddings generated",
        ]
        
        for log in sample_logs:
            st.text(log)
        
        # Auto-refresh option
        if st.checkbox("Auto-refresh logs (every 5 seconds)"):
            st.info("Auto-refresh is enabled")
        
        # Clear logs button
        if st.button("Clear Logs", use_container_width=True):
            st.info("Logs will be cleared on next refresh")


def create_app() -> StreamlitApp:
    """Create and configure the Streamlit application"""
    
    # Create configuration
    config = AppConfig(
        app_name="Document Chat System",
        app_description="Process documents and ask questions with AI",
        app_icon="📚",
        page_config={
            "layout": "wide",
            "initial_sidebar_state": "expanded",
        },
    )
    
    # Create app
    app = StreamlitApp(config)
    
    # Add pages
    app.add_page(HomePage())
    app.add_page(ChatPage())
    app.add_page(DocumentPage())
    app.add_page(SettingsPage())
    app.add_page(LogsPage())
    
    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
