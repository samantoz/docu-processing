"""Main Streamlit application framework"""

import streamlit as st
from typing import Dict, List, Optional, Callable, Any
from streamlit_ui.core.config import AppConfig
from streamlit_ui.core.page import Page
from streamlit_ui.utils.logger import setup_logger
import logging


class StreamlitApp:
    """Main application class for building modular Streamlit apps"""
    
    def __init__(self, config: AppConfig):
        """
        Initialize the Streamlit application.
        
        Args:
            config: AppConfig instance with application settings
        """
        self.config = config
        self.pages: Dict[str, Page] = {}
        self.navigation_items: List[Dict[str, str]] = []
        self.logger = setup_logger(config.app_name, config.log_level)
        self.current_page: Optional[str] = None
        self.callbacks: Dict[str, List[Callable]] = {
            "on_page_change": [],
            "on_app_start": [],
            "on_app_end": []
        }
        
        self._setup_page()
    
    def _setup_page(self) -> None:
        """Configure the Streamlit page settings"""
        st.set_page_config(
            page_title=self.config.page_config.get("page_title", self.config.app_name),
            page_icon=self.config.page_config.get("page_icon", self.config.app_icon),
            layout=self.config.page_config.get("layout", "wide"),
            initial_sidebar_state=self.config.page_config.get("initial_sidebar_state", "expanded"),
        )
        
        # Apply custom CSS if needed
        self._apply_custom_styling()
    
    def _apply_custom_styling(self) -> None:
        """Apply custom styling to the app"""
        custom_css = """
        <style>
        .main-header {
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 1rem;
        }
        .sidebar-header {
            font-size: 1.5rem;
            font-weight: bold;
            margin-bottom: 1rem;
        }
        </style>
        """
        st.markdown(custom_css, unsafe_allow_html=True)
    
    def add_page(self, page: Page) -> "StreamlitApp":
        """
        Add a page to the application.
        
        Args:
            page: Page instance to add
            
        Returns:
            Self for method chaining
        """
        self.pages[page.name] = page
        self.navigation_items.append({
            "name": page.name,
            "icon": page.icon,
            "display": page.get_display_name()
        })
        self.logger.info(f"Added page: {page.name}")
        return self
    
    def remove_page(self, page_name: str) -> "StreamlitApp":
        """Remove a page from the application"""
        if page_name in self.pages:
            del self.pages[page_name]
            self.navigation_items = [
                item for item in self.navigation_items if item["name"] != page_name
            ]
            self.logger.info(f"Removed page: {page_name}")
        return self
    
    def add_callback(self, event: str, callback: Callable) -> "StreamlitApp":
        """
        Add a callback for an event.
        
        Args:
            event: Event name (on_page_change, on_app_start, on_app_end)
            callback: Callable function to execute
            
        Returns:
            Self for method chaining
        """
        if event in self.callbacks:
            self.callbacks[event].append(callback)
        return self
    
    def _execute_callbacks(self, event: str) -> None:
        """Execute all callbacks for a given event"""
        for callback in self.callbacks.get(event, []):
            try:
                callback()
            except Exception as e:
                self.logger.error(f"Error executing callback for {event}: {str(e)}")
    
    def render_sidebar(self) -> Optional[str]:
        """
        Render the sidebar with navigation and return selected page.
        
        Returns:
            Name of the selected page or None
        """
        if not self.config.sidebar_enabled:
            return None
        
        with st.sidebar:
            st.markdown(f"### {self.config.app_icon} {self.config.app_name}")
            
            if self.config.app_description:
                st.markdown(f"*{self.config.app_description}*")
                st.divider()
            
            # Navigation
            page_names = [item["display"] for item in self.navigation_items]
            selected = st.radio(
                "Navigate to:",
                page_names,
                label_visibility="collapsed"
            )
            
            # Extract page name from display name
            selected_page = None
            for item in self.navigation_items:
                if item["display"] == selected:
                    selected_page = item["name"]
                    break
            
            st.divider()
            
            # Additional sidebar content
            self._render_sidebar_footer()
            
            return selected_page
    
    def _render_sidebar_footer(self) -> None:
        """Render footer content in sidebar"""
        st.caption(f"*Version: {st.session_state.get('app_version', '0.1.0')}*")
        
        # Theme toggle
        if self.config.dark_mode_enabled:
            theme_option = st.radio(
                "Theme:",
                ["Light", "Dark"],
                key="theme_toggle",
                label_visibility="collapsed"
            )
    
    def run(self) -> None:
        """Run the Streamlit application"""
        # Initialize session state
        if "app_initialized" not in st.session_state:
            st.session_state.app_initialized = True
            st.session_state.app_version = "0.1.0"
            self._execute_callbacks("on_app_start")
        
        # Render header
        st.markdown(f"# {self.config.app_icon} {self.config.app_name}")
        if self.config.app_description:
            st.markdown(f"**{self.config.app_description}**")
        
        # Render sidebar and get selected page
        selected_page_name = self.render_sidebar()
        
        # Determine which page to render
        if selected_page_name is None and self.pages:
            # Default to first page
            selected_page_name = list(self.pages.keys())[0]
        
        # Update current page
        if selected_page_name != self.current_page:
            if self.current_page and self.current_page in self.pages:
                self.pages[self.current_page].on_unload()
            self.current_page = selected_page_name
            self._execute_callbacks("on_page_change")
            if self.current_page and self.current_page in self.pages:
                self.pages[self.current_page].on_init()
        
        # Render the selected page
        st.divider()
        
        if self.current_page and self.current_page in self.pages:
            page = self.pages[self.current_page]
            page.on_load()
            
            try:
                page.render()
            except Exception as e:
                st.error(f"Error rendering page: {str(e)}")
                self.logger.error(f"Error rendering page {self.current_page}: {str(e)}")
        elif self.pages:
            st.info("Select a page from the sidebar to begin.")
        else:
            st.warning("No pages have been added to the application.")
    
    def get_page(self, name: str) -> Optional[Page]:
        """Get a page by name"""
        return self.pages.get(name)
    
    def get_pages(self) -> Dict[str, Page]:
        """Get all pages"""
        return self.pages.copy()
    
    def get_logger(self) -> logging.Logger:
        """Get the application logger"""
        return self.logger
