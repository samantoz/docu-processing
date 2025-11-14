"""Page abstraction for Streamlit applications"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Callable
import streamlit as st


class Page(ABC):
    """Abstract base class for Streamlit pages"""
    
    def __init__(self, name: str, icon: str = "📄", description: str = ""):
        """
        Initialize a page.
        
        Args:
            name: Display name of the page
            icon: Emoji icon for the page
            description: Brief description of the page
        """
        self.name = name
        self.icon = icon
        self.description = description
        self.state = {}
    
    @abstractmethod
    def render(self) -> None:
        """Render the page content. Must be implemented by subclasses."""
        pass
    
    def on_init(self) -> None:
        """Called when the page is first initialized. Override in subclasses."""
        pass
    
    def on_load(self) -> None:
        """Called every time the page loads. Override in subclasses."""
        pass
    
    def on_unload(self) -> None:
        """Called when navigating away from the page. Override in subclasses."""
        pass
    
    def get_display_name(self) -> str:
        """Get the display name with icon"""
        return f"{self.icon} {self.name}"
    
    def set_state(self, key: str, value: Any) -> None:
        """Set page state"""
        self.state[key] = value
    
    def get_state(self, key: str, default: Any = None) -> Any:
        """Get page state"""
        return self.state.get(key, default)
    
    def render_header(self, title: Optional[str] = None) -> None:
        """Render a standard header for the page"""
        if title is None:
            title = self.name
        
        st.title(title)
        if self.description:
            st.markdown(self.description)
    
    def render_footer(self, text: str = "") -> None:
        """Render a footer with optional text"""
        st.divider()
        if text:
            st.caption(text)
