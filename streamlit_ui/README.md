# Streamlit UI Framework

A modular, reusable Streamlit application framework designed for rapid development of web UIs. This framework emphasizes modularity and reusability, making it suitable for building multi-page applications that can be easily adapted for different projects.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Guide](#usage-guide)
  - [Creating an Application](#creating-an-application)
  - [Building Pages](#building-pages)
  - [Using Components](#using-components)
  - [Managing State](#managing-state)
  - [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Advanced Usage](#advanced-usage)
- [Examples](#examples)
- [API Reference](#api-reference)
- [Contributing](#contributing)

---

## Overview

The Streamlit UI Framework provides a structured foundation for building modular Streamlit applications. It abstracts common patterns and provides reusable components, allowing developers to focus on business logic rather than boilerplate code.

### Why Use This Framework?

- **Modular Design**: Organize your application into logical, reusable pages
- **Separation of Concerns**: Clear separation between configuration, pages, and components
- **Reusability**: Use pages and components across different projects
- **Type Safety**: Built with Python type hints for better IDE support
- **Configuration Management**: Centralized configuration handling
- **State Management**: Simplified session state management utilities
- **Logging**: Built-in logging support

---

## Features

### Core Features

- ✅ **Multi-page Applications**: Easy navigation between pages with automatic sidebar generation
- ✅ **Page Abstraction**: Abstract `Page` class for consistent page structure
- ✅ **Configuration Management**: `AppConfig` class for centralized settings
- ✅ **Component Library**: Pre-built reusable UI components
- ✅ **State Management**: Utilities for managing application and page state
- ✅ **Session Handling**: Built-in session state management
- ✅ **Logging**: Application-level logging support
- ✅ **Callbacks**: Hook system for application lifecycle events
- ✅ **Theming**: Support for light/dark themes

### Built-in Components

- Info/Success/Error/Warning boxes
- Metric cards and displays
- Tabs and expandable sections
- Progress bars and badges
- Form builder for easy form creation
- Multi-column layouts
- Button groups

---

## Architecture

```
streamlit_ui/
├── __init__.py                 # Package initialization
├── core/                       # Core framework components
│   ├── __init__.py
│   ├── app.py                 # StreamlitApp main class
│   ├── page.py                # Page abstract base class
│   └── config.py              # AppConfig configuration class
├── components/                # Reusable UI components
│   └── __init__.py            # Component utilities and functions
├── utils/                     # Utility modules
│   ├── __init__.py
│   ├── logger.py              # Logging utilities
│   └── state.py               # State management helpers
├── pages/                     # Directory for application pages
│   └── __init__.py
└── example_app.py             # Example application
```

---

## Installation

### Prerequisites

- Python 3.8+
- pip or uv (recommended)

### Step 1: Install Streamlit

```bash
# Using pip
pip install streamlit>=1.28.0

# Using uv
uv pip install streamlit>=1.28.0
```

### Step 2: Install Additional Dependencies

```bash
# Using pip
pip install python-dotenv

# Using uv
uv pip install python-dotenv
```

### Step 3: Framework is Ready

The framework is included in the `streamlit_ui/` directory. No additional installation needed!

### Complete Requirements (Optional)

Create a `requirements.txt` for your Streamlit projects:

```text
streamlit>=1.28.0
python-dotenv>=1.0.0
```

Install with:
```bash
pip install -r requirements.txt
```

---

## Quick Start

### Running the Example Application

```bash
# From the docu-processing directory
streamlit run streamlit_ui/example_app.py
```

The application will open in your browser at `http://localhost:8501`

### Creating Your First App

```python
from streamlit_ui.core.app import StreamlitApp
from streamlit_ui.core.page import Page
from streamlit_ui.core.config import AppConfig
import streamlit as st


class MyPage(Page):
    def __init__(self):
        super().__init__(name="My Page", icon="📄")
    
    def render(self):
        self.render_header()
        st.write("Hello, World!")


# Create configuration
config = AppConfig(
    app_name="My App",
    app_description="My first app using the framework"
)

# Create and configure app
app = StreamlitApp(config)
app.add_page(MyPage())

# Run the app
if __name__ == "__main__":
    app.run()
```

Run with:
```bash
streamlit run your_app.py
```

---

## Usage Guide

### Creating an Application

#### Step 1: Configure the Application

```python
from streamlit_ui.core.config import AppConfig

config = AppConfig(
    app_name="Document Chat System",
    app_description="Chat with your documents using AI",
    app_icon="📚",
    page_config={
        "layout": "wide",
        "initial_sidebar_state": "expanded",
    },
    theme="light",
    dark_mode_enabled=True,
    log_level="INFO"
)
```

#### Step 2: Create the Application

```python
from streamlit_ui.core.app import StreamlitApp

app = StreamlitApp(config)
```

#### Step 3: Add Pages and Run

```python
app.add_page(HomePage())
app.add_page(ChatPage())
app.add_page(SettingsPage())

if __name__ == "__main__":
    app.run()
```

### Building Pages

#### Basic Page

```python
from streamlit_ui.core.page import Page
import streamlit as st


class HomePage(Page):
    def __init__(self):
        super().__init__(
            name="Home",
            icon="🏠",
            description="Welcome to my app"
        )
    
    def render(self):
        # render_header() is a helper method
        self.render_header()
        
        st.markdown("## Your content here")
        st.write("This is a basic page")
        
        # Optional footer
        self.render_footer("Made with ❤️ using Streamlit")
```

#### Page with State Management

```python
from streamlit_ui.utils.state import StateManager

class ChatPage(Page):
    def __init__(self):
        super().__init__(name="Chat", icon="💬")
        self.state_manager = StateManager("chat_page")
    
    def on_init(self):
        """Called when page is first initialized"""
        if not self.state_manager.get("initialized"):
            self.state_manager.set("messages", [])
            self.state_manager.set("initialized", True)
    
    def render(self):
        self.render_header()
        
        messages = self.state_manager.get("messages", [])
        
        # Display messages
        for msg in messages:
            st.write(msg)
        
        # Input
        if new_msg := st.chat_input("Type a message"):
            messages.append(new_msg)
            self.state_manager.set("messages", messages)
            st.rerun()
```

#### Page with Lifecycle Hooks

```python
class DataPage(Page):
    def on_init(self):
        """Called once when page is first loaded"""
        st.session_state.data = load_data()
    
    def on_load(self):
        """Called every time the page renders"""
        st.write(f"Page loaded at {time.now()}")
    
    def on_unload(self):
        """Called when navigating away from page"""
        cleanup_resources()
    
    def render(self):
        self.render_header()
        st.dataframe(st.session_state.data)
```

### Using Components

#### Basic Components

```python
from streamlit_ui.components import (
    render_info_box,
    render_success_box,
    render_error_box,
    render_warning_box,
)

# Display messages
render_info_box("This is an information message")
render_success_box("Operation completed successfully!")
render_error_box("An error occurred")
render_warning_box("Please be careful")
```

#### Metric Cards

```python
from streamlit_ui.components import render_metric_card, render_key_value_display

# Single metric
render_metric_card("Revenue", "$10,000", "+10%")

# Multiple metrics
data = {
    "Users": 1234,
    "Revenue": "$50k",
    "Growth": "+15%"
}
render_key_value_display(data)
```

#### Forms with FormBuilder

```python
from streamlit_ui.components import FormBuilder

form = FormBuilder()
form.add_text_input("Name", "name")
form.add_text_area("Description", "description", height=100)
form.add_selectbox("Category", ["Option 1", "Option 2"], "category")
form.add_slider("Count", 0, 100, "count")

values = form.render()

if st.button("Submit"):
    st.write(values)
```

#### Tabs

```python
from streamlit_ui.components import render_tabs

def tab1_content():
    st.write("Content for tab 1")

def tab2_content():
    st.write("Content for tab 2")

render_tabs({
    "Tab 1": tab1_content,
    "Tab 2": tab2_content
})
```

#### Two-Column Layout

```python
from streamlit_ui.components import render_two_column_layout

def left():
    st.write("Left column")

def right():
    st.write("Right column")

render_two_column_layout(left, right, ratio=(1, 2))
```

### Managing State

#### Simple State Management

```python
from streamlit_ui.utils.state import SessionState

# Set a value
SessionState.set("user_name", "John")

# Get a value
name = SessionState.get("user_name", "Unknown")

# Check existence
if SessionState.exists("user_name"):
    st.write(f"Welcome, {name}!")

# Delete a value
SessionState.delete("user_name")

# Clear all state
# SessionState.clear()
```

#### Namespace State Management

```python
from streamlit_ui.utils.state import StateManager

# Create a manager for a specific namespace
state = StateManager("my_app")

# Set and get values
state.set("count", 0)
state.set("data", {"key": "value"})

count = state.get("count")
data = state.get("data")

# Clear namespace
state.clear()

# Get all values
all_values = state.get_all()
```

### Configuration

#### Creating Custom Configuration

```python
from streamlit_ui.core.config import AppConfig

config = AppConfig(
    app_name="My Application",
    app_description="A sample application",
    app_icon="🎯",
    page_config={
        "layout": "centered",
        "initial_sidebar_state": "collapsed",
    },
    theme="dark",
    primary_color="#FF5733",
    secondary_color="#33FF57",
    sidebar_enabled=True,
    dark_mode_enabled=True,
    log_level="DEBUG",
    log_file="app.log",
    cache_enabled=True,
    cache_ttl=7200
)
```

#### Loading Configuration from Environment

```python
config = AppConfig.from_env(env_file=".env")

# Access environment variables
api_key = config.get_env_var("API_KEY", default="")
```

#### .env File Example

```env
# Application Settings
APP_NAME=My Document Processor
APP_ICON=📚

# API Configuration
OPENAI_API_KEY=sk-...
OLLAMA_BASE_URL=http://localhost:11434

# Database
CHROMA_DB_PATH=./chroma_db

# Logging
LOG_LEVEL=INFO
```

---

## Project Structure

### Organizing Your Application

Recommended structure for larger applications:

```
your_project/
├── streamlit_app.py           # Main entry point
├── pages/
│   ├── home.py
│   ├── chat.py
│   ├── settings.py
│   └── documents.py
├── utils/
│   ├── embeddings.py
│   ├── database.py
│   └── llm.py
├── config/
│   ├── settings.py
│   └── constants.py
├── data/
│   └── documents/
├── requirements.txt
├── .env
└── README.md
```

### Main Entry Point Example

```python
# streamlit_app.py
from streamlit_ui.core.app import StreamlitApp
from streamlit_ui.core.config import AppConfig
from pages.home import HomePage
from pages.chat import ChatPage
from pages.documents import DocumentsPage
from pages.settings import SettingsPage


def create_app():
    config = AppConfig(
        app_name="Document Chat System",
        app_description="Process documents and chat with AI",
        app_icon="📚",
        env_file=".env"
    )
    
    app = StreamlitApp(config)
    
    # Add pages
    app.add_page(HomePage())
    app.add_page(ChatPage())
    app.add_page(DocumentsPage())
    app.add_page(SettingsPage())
    
    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
```

---

## Advanced Usage

### Application Callbacks

```python
# Setup callbacks
def on_app_start():
    st.session_state.initialized = True
    st.write("App initialized!")

def on_page_change():
    st.write(f"Page changed to {app.current_page}")

app.add_callback("on_app_start", on_app_start)
app.add_callback("on_page_change", on_page_change)
```

### Logging

```python
from streamlit_ui.utils.logger import setup_logger

# Create logger
logger = setup_logger(
    name="MyApp",
    level="DEBUG",
    log_file="app.log"
)

# Use logger
logger.info("Application started")
logger.warning("This is a warning")
logger.error("An error occurred")

# Or use app's logger
logger = app.get_logger()
```

### Dynamic Page Management

```python
# Add pages dynamically
if condition:
    app.add_page(DynamicPage())

# Remove pages
app.remove_page("Old Page")

# Get page references
pages = app.get_pages()
specific_page = app.get_page("Home")
```

### Custom Styling

Override the `_apply_custom_styling()` method:

```python
class CustomApp(StreamlitApp):
    def _apply_custom_styling(self):
        super()._apply_custom_styling()
        
        custom_css = """
        <style>
        .custom-header { color: #FF5733; }
        .custom-button { background-color: #33FF57; }
        </style>
        """
        st.markdown(custom_css, unsafe_allow_html=True)
```

---

## Examples

### Example 1: Simple Blog Application

```python
from streamlit_ui.core.app import StreamlitApp
from streamlit_ui.core.page import Page
from streamlit_ui.core.config import AppConfig
import streamlit as st


class BlogPage(Page):
    def render(self):
        self.render_header("Welcome to My Blog")
        
        st.markdown("""
        # Latest Posts
        
        ### Post 1: Getting Started with Streamlit
        Learn how to build interactive web apps with Streamlit...
        
        ### Post 2: Advanced Streamlit Patterns
        Explore advanced patterns and best practices...
        """)


class AboutPage(Page):
    def render(self):
        self.render_header("About Me")
        st.write("I'm a developer who loves Streamlit!")


if __name__ == "__main__":
    config = AppConfig(
        app_name="My Blog",
        app_icon="📝"
    )
    
    app = StreamlitApp(config)
    app.add_page(BlogPage("Blog", "📄", "Read my latest posts"))
    app.add_page(AboutPage("About", "👤", "Learn about me"))
    
    app.run()
```

### Example 2: Data Analysis Dashboard

```python
from streamlit_ui.core.app import StreamlitApp
from streamlit_ui.core.page import Page
from streamlit_ui.core.config import AppConfig
from streamlit_ui.components import render_metric_card
import streamlit as st
import pandas as pd


class DashboardPage(Page):
    def render(self):
        self.render_header("Sales Dashboard")
        
        # Load data
        data = pd.DataFrame({
            "Date": pd.date_range("2025-01-01", periods=30),
            "Revenue": [1000 + i*100 for i in range(30)],
            "Users": [50 + i*5 for i in range(30)]
        })
        
        # Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Revenue", f"${data['Revenue'].sum():,.0f}")
        with col2:
            st.metric("Total Users", f"{data['Users'].sum():.0f}")
        with col3:
            st.metric("Avg Daily Revenue", f"${data['Revenue'].mean():,.0f}")
        
        # Charts
        st.line_chart(data.set_index("Date"))
        
        # Data table
        st.dataframe(data)


if __name__ == "__main__":
    config = AppConfig(app_name="Sales Dashboard", app_icon="📊")
    app = StreamlitApp(config)
    app.add_page(DashboardPage("Dashboard"))
    app.run()
```

---

## API Reference

### StreamlitApp

Main application class.

#### Methods

| Method | Description |
|--------|-------------|
| `add_page(page: Page)` | Add a page to the application |
| `remove_page(page_name: str)` | Remove a page from the application |
| `add_callback(event: str, callback: Callable)` | Add a callback for an event |
| `render_sidebar()` | Render the sidebar navigation |
| `run()` | Run the application |
| `get_page(name: str)` | Get a specific page |
| `get_pages()` | Get all pages |
| `get_logger()` | Get the application logger |

### Page

Abstract base class for pages.

#### Methods

| Method | Description |
|--------|-------------|
| `render()` | Render page content (required) |
| `on_init()` | Called once when page is initialized |
| `on_load()` | Called every time page loads |
| `on_unload()` | Called when navigating away |
| `render_header(title)` | Render standard page header |
| `render_footer(text)` | Render standard page footer |
| `set_state(key, value)` | Set page state |
| `get_state(key, default)` | Get page state |

### AppConfig

Configuration dataclass.

#### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `app_name` | str | Application name |
| `app_description` | str | Application description |
| `app_icon` | str | Application icon (emoji) |
| `page_config` | Dict | Streamlit page configuration |
| `theme` | str | Theme (light/dark) |
| `sidebar_enabled` | bool | Enable/disable sidebar |
| `dark_mode_enabled` | bool | Enable/disable dark mode toggle |
| `log_level` | str | Logging level |
| `cache_enabled` | bool | Enable caching |
| `cache_ttl` | int | Cache TTL in seconds |

---

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## License

This framework is licensed under the MIT License.

---

## Support

For issues, questions, or suggestions:

1. Check the examples and usage guide
2. Review the API reference
3. Open an issue on the repository

---

## Next Steps

- Build your first app with the framework
- Explore the example application in `streamlit_ui/example_app.py`
- Customize the components for your needs
- Create reusable pages for other projects
