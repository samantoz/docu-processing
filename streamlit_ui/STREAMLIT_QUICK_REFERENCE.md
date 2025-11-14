# Streamlit UI Framework - Quick Reference

## 🚀 Quick Start (30 seconds)

```bash
# Install
pip install streamlit>=1.28.0 python-dotenv

# Run example
streamlit run streamlit_ui/example_app.py

# Create your app
cp streamlit_ui/app_template.py my_app.py
streamlit run my_app.py
```

## 📁 File Structure

```
streamlit_ui/
├── core/                 # Framework core (app, page, config)
├── components/           # Pre-built UI components
├── utils/                # Helpers (logging, state)
├── pages/                # Your app pages go here
├── example_app.py        # Working example
├── app_template.py       # Template for new apps
├── README.md             # Full documentation
└── INDEX.md              # Overview
```

## 💻 Basic App Template

```python
from streamlit_ui.core.app import StreamlitApp
from streamlit_ui.core.page import Page
from streamlit_ui.core.config import AppConfig
import streamlit as st

class HomePage(Page):
    def __init__(self):
        super().__init__(name="Home", icon="🏠")
    
    def render(self):
        self.render_header()
        st.write("Hello, World!")

config = AppConfig(app_name="My App")
app = StreamlitApp(config)
app.add_page(HomePage())

if __name__ == "__main__":
    app.run()
```

## 🎯 Core Classes

### StreamlitApp
```python
app = StreamlitApp(config)
app.add_page(page)
app.remove_page("Page Name")
app.add_callback("on_app_start", callback_func)
app.run()
```

### Page
```python
class MyPage(Page):
    def __init__(self):
        super().__init__(name="My Page", icon="📄")
    
    def render(self):
        pass
    
    def on_init(self):      # Called once
        pass
    
    def on_load(self):      # Called every time
        pass
    
    def on_unload(self):    # Called when leaving
        pass
```

### AppConfig
```python
config = AppConfig(
    app_name="My App",
    app_description="Description",
    app_icon="🚀",
    theme="light",
    log_level="INFO"
)
```

## 🧩 Common Components

### Message Boxes
```python
from streamlit_ui.components import (
    render_info_box,
    render_success_box,
    render_error_box,
    render_warning_box
)

render_info_box("Info message")
render_success_box("Success!")
render_error_box("Error occurred")
render_warning_box("Be careful")
```

### Metrics
```python
from streamlit_ui.components import render_metric_card
render_metric_card("Label", "Value", "+10%")
```

### Forms
```python
from streamlit_ui.components import FormBuilder

form = FormBuilder()
form.add_text_input("Name", "name")
form.add_selectbox("Category", ["A", "B"], "category")
form.add_slider("Count", 0, 100, "count")
values = form.render()
```

### Tabs
```python
from streamlit_ui.components import render_tabs

render_tabs({
    "Tab 1": lambda: st.write("Content 1"),
    "Tab 2": lambda: st.write("Content 2")
})
```

### Two Columns
```python
from streamlit_ui.components import render_two_column_layout

render_two_column_layout(
    lambda: st.write("Left"),
    lambda: st.write("Right")
)
```

## 🔐 State Management

### Simple
```python
from streamlit_ui.utils.state import SessionState

SessionState.set("key", "value")
value = SessionState.get("key")
SessionState.delete("key")
```

### Namespaced
```python
from streamlit_ui.utils.state import StateManager

state = StateManager("my_namespace")
state.set("key", "value")
value = state.get("key")
state.clear()
```

## 📝 Configuration

### In Code
```python
config = AppConfig(
    app_name="Name",
    app_icon="🚀",
    primary_color="#1f77b4",
    dark_mode_enabled=True,
    log_level="INFO"
)
```

### From Environment
```python
config = AppConfig.from_env(".env")
api_key = config.get_env_var("API_KEY", "default")
```

### .env File
```env
APP_NAME=My App
LOG_LEVEL=INFO
API_KEY=secret
```

## 🪵 Logging

```python
from streamlit_ui.utils.logger import setup_logger

logger = setup_logger("MyApp", "INFO", "app.log")
logger.info("Message")
logger.warning("Warning")
logger.error("Error")

# Or use app logger
logger = app.get_logger()
```

## 🔄 Callbacks

```python
def on_start():
    st.write("App started!")

def on_page_change():
    st.write(f"Changed to {app.current_page}")

app.add_callback("on_app_start", on_start)
app.add_callback("on_page_change", on_page_change)
```

## 📊 Page Helpers

```python
class MyPage(Page):
    def render(self):
        # Render header with title
        self.render_header()
        
        # Your content
        st.write("Content")
        
        # Render footer
        self.render_footer("Made with ❤️")
        
        # Manage state
        self.set_state("key", "value")
        value = self.get_state("key")
```

## 🎨 Layout Components

```python
from streamlit_ui.components import (
    render_expandable_section,
    render_button_group,
    render_progress_bar,
    render_badge,
    render_separator
)

render_expandable_section("Title", lambda: st.write("Content"))
render_progress_bar(75, 100, "Progress")
render_badge("Active", "#1f77b4")
render_button_group([
    ("Button 1", callback1, "key1"),
    ("Button 2", callback2, "key2")
])
```

## 🚀 Running Your App

```bash
# Basic
streamlit run app.py

# Custom port
streamlit run app.py --server.port 8502

# Development with reload
streamlit run app.py --logger.level=debug

# Production
streamlit run app.py --server.headless true
```

## 📚 Documentation

- **Full Docs**: `streamlit_ui/README.md`
- **Example App**: `streamlit_ui/example_app.py`
- **Template**: `streamlit_ui/app_template.py`
- **Index**: `streamlit_ui/INDEX.md`
- **Setup**: `STREAMLIT_SETUP.md`

## 💡 Tips & Tricks

### Cache Data
```python
@st.cache_data
def load_data():
    return data
```

### Use Session State
```python
if "key" not in st.session_state:
    st.session_state.key = initial_value
```

### Conditional Rendering
```python
if condition:
    st.write("Show this")
else:
    st.warning("Show this instead")
```

### Forms
```python
with st.form("form_key"):
    name = st.text_input("Name")
    submitted = st.form_submit_button("Submit")
    if submitted:
        process(name)
```

### Spinners
```python
with st.spinner("Loading..."):
    result = expensive_operation()
st.success("Done!")
```

## 🔗 Common Patterns

### Multi-Page App
```python
for page in [HomePage(), ChatPage(), SettingsPage()]:
    app.add_page(page)
```

### Dynamic Pages
```python
if show_advanced:
    app.add_page(AdvancedPage())
```

### State Across Pages
```python
# Shared state via session_state
st.session_state.shared_data = value

# Or use StateManager for namespace isolation
state = StateManager("app_level")
```

### Error Handling
```python
try:
    result = risky_operation()
except Exception as e:
    st.error(f"Error: {str(e)}")
```

## 📦 Dependencies

```
streamlit>=1.28.0
python-dotenv>=1.0.0
pandas>=2.0.0 (optional)
numpy>=1.24.0 (optional)
```

Install:
```bash
pip install -r streamlit_ui/requirements.txt
```

## ❓ Common Issues

| Issue | Solution |
|-------|----------|
| Port in use | `streamlit run app.py --server.port 8502` |
| Cache issues | `streamlit cache clear` |
| Import errors | Ensure `streamlit_ui/` is in path or copy locally |
| State lost on rerun | Use `st.session_state` or `StateManager` |

## 🎓 Learning Path

1. Read `STREAMLIT_SETUP.md`
2. Run example app: `streamlit run streamlit_ui/example_app.py`
3. Copy template: `cp streamlit_ui/app_template.py my_app.py`
4. Modify and run
5. Read `README.md` for deeper understanding
6. Build your own pages and components

## 📖 Resources

- **Streamlit Docs**: https://docs.streamlit.io/
- **Streamlit Community**: https://discuss.streamlit.io/
- **Framework Docs**: `streamlit_ui/README.md`
- **Example Code**: `streamlit_ui/example_app.py`

---

**Happy Building! 🎉**
