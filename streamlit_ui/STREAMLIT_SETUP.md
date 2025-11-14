# Streamlit UI Framework - Quick Setup Guide

## 📋 Prerequisites

- Python 3.8+
- pip or uv (recommended)

## 🚀 Installation & Setup

### Step 1: Install Streamlit

```bash
# Using pip
pip install streamlit>=1.28.0 python-dotenv

# Using uv
uv pip install streamlit>=1.28.0 python-dotenv
```

### Step 2: Run the Example Application

```bash
# From the docu-processing directory
streamlit run streamlit_ui/example_app.py
```

The app will open at `http://localhost:8501`

## 📖 Basic Usage

### Creating Your First Application

1. **Create a new Python file** (`my_app.py`):

```python
from streamlit_ui.core.app import StreamlitApp
from streamlit_ui.core.page import Page
from streamlit_ui.core.config import AppConfig
import streamlit as st


class HomePage(Page):
    def __init__(self):
        super().__init__(name="Home", icon="🏠")
    
    def render(self):
        self.render_header("Welcome!")
        st.write("This is my first Streamlit app using the framework")


if __name__ == "__main__":
    config = AppConfig(
        app_name="My App",
        app_description="My first application"
    )
    
    app = StreamlitApp(config)
    app.add_page(HomePage())
    app.run()
```

2. **Run your app**:

```bash
streamlit run my_app.py
```

## 🎨 Key Features to Explore

### Multi-Page Navigation
Pages are automatically added to the sidebar with icons and descriptions.

### Reusable Components
```python
from streamlit_ui.components import FormBuilder, render_tabs, render_info_box

# Build forms easily
form = FormBuilder()
form.add_text_input("Name", "name")
values = form.render()

# Display messages
render_info_box("This is an information message")
```

### State Management
```python
from streamlit_ui.utils.state import StateManager

state = StateManager("my_page")
state.set("count", 0)
count = state.get("count")
```

## 📁 Project Structure

```
streamlit_ui/
├── core/               # Core framework (app, page, config)
├── components/         # Reusable UI components
├── utils/              # Utilities (logging, state management)
├── pages/              # Your application pages
├── example_app.py      # Example application
└── README.md           # Full documentation
```

## 🎯 Common Tasks

### Add a New Page

```python
class MyPage(Page):
    def __init__(self):
        super().__init__(
            name="My Page",
            icon="📄",
            description="This is my page"
        )
    
    def render(self):
        self.render_header()
        # Your content here
        st.write("Page content")

app.add_page(MyPage())
```

### Use Session State

```python
from streamlit_ui.utils.state import SessionState

SessionState.set("username", "John")
name = SessionState.get("username")
```

### Add Callbacks

```python
def on_start():
    st.write("App started!")

app.add_callback("on_app_start", on_start)
```

## 🔧 Configuration

Create a `.env` file in your project root:

```env
APP_NAME=My Application
LOG_LEVEL=INFO
OPENAI_API_KEY=your_key_here
```

Load it in your app:

```python
config = AppConfig.from_env(env_file=".env")
```

## 📚 Resources

- **Full Documentation**: See `streamlit_ui/README.md`
- **Example Application**: See `streamlit_ui/example_app.py`
- **Streamlit Docs**: https://docs.streamlit.io/

## ✨ Tips

- Use `@st.cache_data` for expensive computations
- Leverage `st.session_state` for persistent data across reruns
- Use pages for organizing complex applications
- Check the example app for more patterns and examples

## 🐛 Troubleshooting

### Port Already in Use
```bash
streamlit run app.py --server.port 8502
```

### Clear Cache
```bash
streamlit cache clear
```

### Check Streamlit Version
```bash
streamlit --version
```

## 📝 Next Steps

1. Explore the example application
2. Read the full documentation in `streamlit_ui/README.md`
3. Build your first multi-page application
4. Customize components for your needs

---

**Happy building!** 🎉
