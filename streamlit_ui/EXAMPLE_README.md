# Document Chat System - Example Application

This is an example Streamlit application demonstrating the capabilities of the **Streamlit UI Framework**. It showcases a document processing and AI chat interface system.

## 🎯 Features

This example application includes:

### Pages

1. **Home (🏠)**
   - Overview of the application
   - Key features showcase
   - Quick statistics

2. **Chat (💬)**
   - Interactive chat interface
   - Chat history management
   - AI-powered responses (ready for RAG integration)

3. **Documents (📚)**
   - Upload PDF documents
   - Configure processing options
   - Document processing with chunking
   - Batch processing support

4. **Settings (⚙️)**
   - Embedding provider configuration
     - OpenAI
     - Ollama
     - Azure OpenAI
   - ChromaDB settings
   - Easy settings persistence

5. **Logs (📋)**
   - View application logs
   - Monitor processing activities
   - Filter log types
   - Auto-refresh capability

## 🚀 Running the Example

### Prerequisites

```bash
# Install required packages
pip install streamlit>=1.28.0 python-dotenv
```

### Start the Application

```bash
# From the docu-processing directory
streamlit run streamlit_ui/example_app.py
```

The application will open in your default browser at `http://localhost:8501`

## 📖 Using the Application

### Home Page
- Read the welcome message and feature overview
- Check the quick statistics (currently showing sample data)

### Chat Page
- Type your questions about documents
- View chat history
- Clear conversation history with the button

### Documents Page
1. **Upload Documents**
   - Click "Upload PDF documents" button
   - Select one or multiple PDF files

2. **Configure Processing**
   - Adjust chunk size (100-5000 characters)
   - Set chunk overlap (0-500 characters)

3. **Process**
   - Click "Process Documents"
   - Monitor processing status

### Settings Page
1. **Select Embedding Provider**
   - OpenAI (requires API key)
   - Ollama (requires local Ollama installation)
   - Azure OpenAI (requires credentials)

2. **Configure Provider Settings**
   - Enter API keys or URLs as needed
   - Select embedding models

3. **Database Configuration**
   - Set ChromaDB path
   - Configure collection name

4. **Save Settings**
   - Click "Save Settings" to persist configuration

### Logs Page
- View recent application logs
- Filter by log type
- Enable auto-refresh for real-time monitoring

## 🔧 Framework Features Used

This example demonstrates:

### Core Features
- ✅ Multi-page application structure
- ✅ Page navigation and sidebar
- ✅ Session state management
- ✅ Page lifecycle hooks (on_init, on_load, on_unload)

### Components
- ✅ Info/Success/Error/Warning message boxes
- ✅ Chat interface
- ✅ Form inputs (text, selectbox, slider)
- ✅ File upload handling
- ✅ Metric displays
- ✅ Multi-column layouts
- ✅ Expandable sections

### Utilities
- ✅ State management (SessionState and StateManager)
- ✅ Application configuration
- ✅ Logging setup

## 📝 Code Structure

```python
# Each page is a class inheriting from Page
class ChatPage(Page):
    def __init__(self):
        super().__init__(name="Chat", icon="💬")
    
    def render(self):
        # Page content goes here
        pass

# Application setup
config = AppConfig(app_name="Document Chat System", ...)
app = StreamlitApp(config)
app.add_page(ChatPage())
app.run()
```

## 🔌 Integration Points

The example is ready for integration with:

### Chat & RAG
- Replace the mock AI response in ChatPage with actual LangChain/RAG queries
- Connect to ChromaDB for document retrieval
- Use OpenAI/Ollama APIs for responses

### Document Processing
- Integrate with PDF conversion (docling)
- Add document chunking with LangChain
- Store embeddings in ChromaDB

### Settings Management
- Save configuration to .env or database
- Apply settings to embedding and chat providers
- Dynamically update application behavior

## 📚 Example Integration Code

### Extending the Chat Page

```python
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

class ChatPage(Page):
    def __init__(self):
        super().__init__(name="Chat", icon="💬")
        self.vectorstore = None
        self.retriever = None
    
    def on_init(self):
        # Initialize retriever
        embeddings = OpenAIEmbeddings()
        self.vectorstore = Chroma(
            persist_directory="./chroma_db",
            embedding_function=embeddings
        )
        self.retriever = self.vectorstore.as_retriever()
    
    def render(self):
        self.render_header()
        
        if prompt := st.chat_input("Ask about your documents"):
            # Retrieve relevant documents
            docs = self.retriever.get_relevant_documents(prompt)
            
            # Generate response with RAG
            response = generate_response(prompt, docs)
            
            st.write(response)
```

### Extending the Documents Page

```python
from scripts.pdf_to_markdown import convert_pdf_to_markdown
from scripts.chunk_documents import chunk_text

class DocumentPage(Page):
    def render(self):
        self.render_header()
        
        if uploaded_files := st.file_uploader("Upload PDFs"):
            for file in uploaded_files:
                # Convert PDF to markdown
                markdown = convert_pdf_to_markdown(file)
                
                # Chunk the document
                chunks = chunk_text(markdown, chunk_size=1000, overlap=200)
                
                # Store chunks and embeddings
                store_embeddings(chunks)
```

## 🎨 Customization

### Styling
Modify colors and themes in AppConfig:

```python
config = AppConfig(
    primary_color="#FF5733",
    secondary_color="#33FF57",
    theme="dark"
)
```

### Adding New Pages
Create a new page class and add it to the app:

```python
class CustomPage(Page):
    def __init__(self):
        super().__init__(name="Custom", icon="⭐")
    
    def render(self):
        st.write("Custom content")

app.add_page(CustomPage())
```

### Styling Pages
Use custom CSS in page rendering:

```python
def render(self):
    st.markdown("""
    <style>
    .custom-class { color: red; }
    </style>
    """, unsafe_allow_html=True)
```

## 📊 Sample Data

The example includes mock data for demonstration:
- Sample logs (timestamps and messages)
- Mock metrics (0 embeddings, documents, messages)
- Sample chat responses

Replace these with actual data integration as needed.

## 🐛 Troubleshooting

### Port in Use
```bash
streamlit run streamlit_ui/example_app.py --server.port 8502
```

### Clear Application Cache
```bash
streamlit cache clear
```

### View Debug Logs
```bash
streamlit run streamlit_ui/example_app.py --logger.level=debug
```

## 📚 Related Documentation

- **Framework Documentation**: See `streamlit_ui/README.md`
- **Setup Guide**: See `STREAMLIT_SETUP.md`
- **Streamlit Official Docs**: https://docs.streamlit.io/

## 💡 Learning Path

1. **Run the Example**: Execute the example app and explore all pages
2. **Understand Structure**: Review `example_app.py` and page classes
3. **Try Modifications**: Change colors, add new pages, modify content
4. **Integration**: Connect real data sources and APIs
5. **Extend**: Build your own pages and components

## 🎓 Best Practices Demonstrated

- ✅ Clear page organization
- ✅ Consistent naming conventions
- ✅ Descriptive page titles and descriptions
- ✅ Organized sections with headers
- ✅ State management patterns
- ✅ Error handling and user feedback
- ✅ Configuration management
- ✅ Reusable component usage

## 🚀 Next Steps

1. Integrate with your actual document processing pipeline
2. Connect to real embedding providers
3. Add user authentication
4. Implement actual chat functionality with RAG
5. Add more pages for specific use cases
6. Deploy to a hosting platform (Streamlit Cloud, etc.)

---

**Happy building with the Streamlit UI Framework!** 🎉
