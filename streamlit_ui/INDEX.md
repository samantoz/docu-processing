# Streamlit UI Framework - Project Overview

## 📚 What's Included

This directory contains a **modular, reusable Streamlit UI Framework** designed for rapid development of web-based applications. The framework is designed to be framework-agnostic and can be used across different projects.

### Contents

```
streamlit_ui/
├── README.md                  # Comprehensive framework documentation
├── EXAMPLE_README.md          # Example app documentation
├── requirements.txt           # Streamlit dependencies
├── app_template.py            # Template for creating new apps
│
├── core/                      # Core framework components
│   ├── __init__.py
│   ├── app.py                 # Main StreamlitApp class
│   ├── page.py                # Page abstraction
│   └── config.py              # Configuration management
│
├── components/                # Reusable UI components
│   └── __init__.py            # Component library
│
├── utils/                     # Utility modules
│   ├── __init__.py
│   ├── logger.py              # Logging utilities
│   └── state.py               # State management
│
├── pages/                     # Application pages directory
│   └── __init__.py
│
└── example_app.py             # Complete example application
```

## 🎯 Quick Navigation

### For Getting Started
1. **FIRST TIME?** → Read `STREAMLIT_SETUP.md` (in parent directory)
2. **QUICK START** → Run the example app: `streamlit run streamlit_ui/example_app.py`
3. **BUILD YOUR APP** → Copy `app_template.py` and modify it

### For Development
1. **Full Documentation** → `streamlit_ui/README.md`
2. **Example App** → `streamlit_ui/example_app.py`
3. **Template** → `streamlit_ui/app_template.py`

### For Reference
- **API Reference** → See section in `README.md`
- **Code Examples** → See "Examples" section in `README.md`
- **Integration Guide** → See `EXAMPLE_README.md`

## 🚀 Key Features

### Core Framework
- ✅ **Multi-page applications** - Easy navigation between pages
- ✅ **Page abstraction** - Consistent page structure
- ✅ **Configuration management** - Centralized settings
- ✅ **State management** - Simplified session state handling
- ✅ **Callbacks system** - Lifecycle event hooks
- ✅ **Logging** - Built-in logging support

### UI Components
- ✅ Message boxes (info, success, error, warning)
- ✅ Metric cards and displays
- ✅ Form builder with multiple input types
- ✅ Tabs and expandable sections
- ✅ Multi-column layouts
- ✅ Progress bars, badges, separators

### Utilities
- ✅ Session state management
- ✅ Namespace-based state management
- ✅ Logger configuration
- ✅ File utilities

## 📖 How to Use This Framework

### Option 1: Run the Example (Recommended for Learning)

```bash
cd /home/sam/git_repos/docu-processing
streamlit run streamlit_ui/example_app.py
```

This demonstrates:
- Multi-page structure
- All component types
- State management patterns
- Configuration handling

### Option 2: Create Your Own App from Template

1. Copy `app_template.py` to create your app:
```bash
cp streamlit_ui/app_template.py my_app.py
```

2. Modify the template with your pages and logic

3. Run your app:
```bash
streamlit run my_app.py
```

### Option 3: Build from Scratch

1. Create pages by extending the `Page` class
2. Create an `AppConfig` instance
3. Create a `StreamlitApp` instance
4. Add pages to the app
5. Call `app.run()`

See `README.md` for detailed examples.

## 🔧 Framework Architecture

### Core Classes

**StreamlitApp**
- Main application class
- Manages pages and navigation
- Handles sidebar rendering
- Executes callbacks
- Provides logging

**Page**
- Abstract base class for pages
- Defines lifecycle methods (on_init, on_load, on_unload)
- Provides render_header() and render_footer() helpers
- Manages page-level state

**AppConfig**
- Dataclass for application configuration
- Handles Streamlit page settings
- Manages environment variables
- Provides logging configuration

### Component System

The `components/__init__.py` contains utility functions for:
- Message display (info, success, error, warning)
- Metric cards
- Form building
- Layout organization
- Interactive elements

### Utilities

**Logger** (`utils/logger.py`)
- Simple logger setup
- Console and file logging
- Multiple log levels

**State** (`utils/state.py`)
- SessionState for simple session management
- StateManager for namespace-isolated state
- Get/set/delete operations

## 💡 Design Philosophy

This framework emphasizes:

1. **Modularity** - Components can be used independently
2. **Reusability** - Pages and components work across projects
3. **Simplicity** - Easy API, clear abstractions
4. **Type Safety** - Python type hints throughout
5. **Configuration** - Centralized, environment-aware settings
6. **Extensibility** - Easy to extend and customize

## 🎨 Customization

### Adding Custom Pages

```python
class CustomPage(Page):
    def __init__(self):
        super().__init__(name="Custom", icon="⭐")
    
    def render(self):
        self.render_header()
        st.write("Your content here")

app.add_page(CustomPage())
```

### Using Custom Components

```python
from streamlit_ui.components import FormBuilder, render_tabs

form = FormBuilder()
form.add_text_input("Name", "name")
values = form.render()
```

### Creating Reusable Components

Components can be extracted into separate modules for reuse:

```python
# my_components/custom_card.py
def render_custom_card(title, content):
    st.markdown(f"### {title}")
    st.write(content)
```

## 📦 Using in Other Projects

This framework can be easily reused in other projects:

1. **Copy the `streamlit_ui/` directory** to your project
2. **Install dependencies**: `pip install -r streamlit_ui/requirements.txt`
3. **Create your app** using the framework classes
4. **Run with Streamlit**: `streamlit run your_app.py`

### Project Structure for Reuse

```
your_project/
├── streamlit_ui/              # Framework (copied from here)
├── pages/                     # Your page modules
├── utils/                     # Your custom utilities
├── requirements.txt           # Project requirements
├── app.py                     # Main application file
└── .env                       # Configuration
```

## 🧪 Testing the Framework

### Run the Example App
```bash
streamlit run streamlit_ui/example_app.py
```

### Test with the Template
```bash
streamlit run streamlit_ui/app_template.py
```

### Create a Simple Test
```bash
python -c "from streamlit_ui.core.config import AppConfig; print(AppConfig())"
```

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| `README.md` | Comprehensive framework documentation and API reference |
| `EXAMPLE_README.md` | Documentation for the example application |
| `requirements.txt` | Python package dependencies |
| `app_template.py` | Template for creating new applications |
| `example_app.py` | Complete working example application |

## 🔗 Related Files

In the parent directory:
- `STREAMLIT_SETUP.md` - Quick setup guide
- Main project documentation in `readme.md`

## 🚀 Next Steps

1. **Install dependencies**: `pip install streamlit>=1.28.0 python-dotenv`
2. **Run example**: `streamlit run streamlit_ui/example_app.py`
3. **Explore code**: Review `example_app.py` to understand structure
4. **Read documentation**: Check `README.md` for detailed API
5. **Build your app**: Copy `app_template.py` and customize

## 🤝 Using with Other Projects

This framework can be integrated into:

- Document processing systems
- Data analysis dashboards
- Configuration management tools
- Monitoring systems
- Admin panels
- Data visualization apps
- RAG/LLM applications
- And more!

### Integration Example

To use this framework in another project:

```python
# In your project
import sys
sys.path.insert(0, 'path/to/docu-processing')

from streamlit_ui.core.app import StreamlitApp
from streamlit_ui.core.page import Page

# Your pages and app...
```

## 📝 Creating Documentation for Your App

When extending the framework for your project, create similar documentation:

1. Create `YOUR_APP_SETUP.md` - Setup instructions
2. Create `YOUR_APP_README.md` - Full documentation
3. Include code examples
4. Document all custom pages and components

## ❓ Frequently Asked Questions

**Q: Can I use this framework for production apps?**
A: Yes! The framework provides a solid foundation for production Streamlit applications.

**Q: How do I integrate with my existing code?**
A: Pages act as adapters - wrap your logic in a Page class and use it with the framework.

**Q: Can I deploy to Streamlit Cloud?**
A: Yes! Just include the framework files in your repository.

**Q: How do I add authentication?**
A: Implement authentication in the app or page render methods before displaying content.

**Q: Can I modify the framework?**
A: Absolutely! The code is designed to be modified and extended.

## 📞 Support & Resources

- **Framework Code**: Review implementation in `core/`, `components/`, `utils/`
- **Examples**: See `example_app.py` and `app_template.py`
- **Streamlit Docs**: https://docs.streamlit.io/
- **GitHub Issues**: Open issues for bugs or feature requests

## 📄 License

This framework is provided as part of the docu-processing project.

---

**Ready to build?** Start with the Quick Start guide or run the example app! 🎉
