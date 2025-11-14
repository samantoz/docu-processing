"""
Template for creating a new Streamlit application using the UI Framework.
Copy this file and modify it to build your own application.
"""

from streamlit_ui.core.app import StreamlitApp
from streamlit_ui.core.page import Page
from streamlit_ui.core.config import AppConfig
from streamlit_ui.components import render_info_box
from streamlit_ui.utils.state import StateManager
import streamlit as st


# ============================================================================
# PAGE CLASSES - Define your pages here
# ============================================================================

class HomePage(Page):
    """Template home page"""
    
    def __init__(self):
        super().__init__(
            name="Home",
            icon="🏠",
            description="Welcome to my application"
        )
    
    def render(self) -> None:
        """Render the home page"""
        self.render_header("Welcome to My Application")
        
        st.markdown("""
        ### About This Application
        
        This is a template application built with the Streamlit UI Framework.
        
        **Features:**
        - Multi-page navigation
        - Reusable components
        - State management
        - Configuration management
        
        ### Getting Started
        
        1. Explore the other pages using the sidebar
        2. Modify this template for your needs
        3. Add your own pages and logic
        """)
        
        # Example of using components
        render_info_box("This is an info message - replace with your content!")


class DataPage(Page):
    """Template page for data display"""
    
    def __init__(self):
        super().__init__(
            name="Data",
            icon="📊",
            description="View and manage data"
        )
        self.state_manager = StateManager("data_page")
    
    def on_init(self) -> None:
        """Initialize page (called once)"""
        if not self.state_manager.get("initialized"):
            self.state_manager.set("initialized", True)
            st.session_state.sample_data = None
    
    def render(self) -> None:
        """Render the data page"""
        self.render_header("Data Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Load Data")
            if st.button("Load Sample Data"):
                st.session_state.sample_data = self._get_sample_data()
                st.success("Data loaded!")
        
        with col2:
            st.subheader("Actions")
            if st.button("Clear Data"):
                st.session_state.sample_data = None
                st.info("Data cleared")
        
        # Display data if available
        if st.session_state.sample_data is not None:
            st.subheader("Current Data")
            st.dataframe(st.session_state.sample_data)
    
    @staticmethod
    def _get_sample_data():
        """Get sample data"""
        import pandas as pd
        return pd.DataFrame({
            "Name": ["Alice", "Bob", "Charlie"],
            "Value": [10, 20, 30],
            "Status": ["Active", "Inactive", "Active"]
        })


class SettingsPage(Page):
    """Template page for settings"""
    
    def __init__(self):
        super().__init__(
            name="Settings",
            icon="⚙️",
            description="Configure application settings"
        )
    
    def render(self) -> None:
        """Render the settings page"""
        self.render_header("Application Settings")
        
        st.subheader("General Settings")
        
        # Setting 1
        setting1 = st.text_input(
            "Setting 1",
            value=st.session_state.get("setting1", "default"),
            key="setting1_input"
        )
        
        # Setting 2
        setting2 = st.selectbox(
            "Setting 2",
            ["Option A", "Option B", "Option C"],
            index=st.session_state.get("setting2_index", 0),
            key="setting2_select"
        )
        
        # Setting 3
        setting3 = st.slider(
            "Setting 3",
            0.0,
            100.0,
            st.session_state.get("setting3", 50.0),
            key="setting3_slider"
        )
        
        st.divider()
        
        # Save button
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Save Settings"):
                st.session_state.setting1 = setting1
                st.session_state.setting2_index = ["Option A", "Option B", "Option C"].index(setting2)
                st.session_state.setting3 = setting3
                st.success("Settings saved!")
        
        with col2:
            if st.button("Reset to Defaults"):
                st.session_state.clear()
                st.info("Settings reset!")


# ============================================================================
# APPLICATION SETUP
# ============================================================================

def create_app() -> StreamlitApp:
    """
    Create and configure the application.
    
    Returns:
        Configured StreamlitApp instance
    """
    # Create configuration
    config = AppConfig(
        app_name="My Application",
        app_description="A template application using the Streamlit UI Framework",
        app_icon="🚀",
        page_config={
            "layout": "wide",
            "initial_sidebar_state": "expanded",
        },
        theme="light",
        dark_mode_enabled=True,
        log_level="INFO"
    )
    
    # Create app instance
    app = StreamlitApp(config)
    
    # Add pages
    app.add_page(HomePage())
    app.add_page(DataPage())
    app.add_page(SettingsPage())
    
    # Optional: Add callbacks
    def on_app_start():
        """Called when app starts"""
        st.session_state.app_started = True
    
    app.add_callback("on_app_start", on_app_start)
    
    return app


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    app = create_app()
    app.run()
