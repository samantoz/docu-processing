"""Common components for Streamlit applications"""

import streamlit as st
from typing import Any, Callable, Dict, List, Optional, Tuple


def render_info_box(message: str, icon: str = "ℹ️") -> None:
    """Render an information box"""
    st.info(f"{icon} {message}")


def render_success_box(message: str, icon: str = "✅") -> None:
    """Render a success message"""
    st.success(f"{icon} {message}")


def render_error_box(message: str, icon: str = "❌") -> None:
    """Render an error message"""
    st.error(f"{icon} {message}")


def render_warning_box(message: str, icon: str = "⚠️") -> None:
    """Render a warning message"""
    st.warning(f"{icon} {message}")


def render_metric_card(label: str, value: Any, delta: Optional[str] = None, col=None) -> None:
    """
    Render a metric card.
    
    Args:
        label: Metric label
        value: Metric value
        delta: Optional delta/change indicator
        col: Optional column to render in
    """
    if col is not None:
        with col:
            st.metric(label, value, delta)
    else:
        st.metric(label, value, delta)


def render_key_value_display(data: Dict[str, Any]) -> None:
    """Render key-value pairs as columns"""
    cols = st.columns(len(data))
    for col, (key, value) in zip(cols, data.items()):
        with col:
            st.metric(key, value)


def render_tabs(tab_data: Dict[str, Callable]) -> None:
    """
    Render tabs with content.
    
    Args:
        tab_data: Dictionary of {tab_name: render_function}
    """
    tabs = st.tabs(list(tab_data.keys()))
    for tab, (tab_name, render_func) in zip(tabs, tab_data.items()):
        with tab:
            render_func()


def render_two_column_layout(
    left_content: Callable,
    right_content: Callable,
    ratio: Tuple[int, int] = (1, 1)
) -> None:
    """
    Render a two-column layout.
    
    Args:
        left_content: Function to render left column
        right_content: Function to render right column
        ratio: Column width ratio
    """
    left_col, right_col = st.columns(ratio)
    
    with left_col:
        left_content()
    
    with right_col:
        right_content()


def render_expandable_section(title: str, content: Callable) -> None:
    """
    Render an expandable section.
    
    Args:
        title: Section title
        content: Function to render content
    """
    with st.expander(title):
        content()


def render_separator(height: int = 2) -> None:
    """Render a separator"""
    st.divider()


def render_badge(text: str, color: str = "#1f77b4") -> None:
    """
    Render a badge.
    
    Args:
        text: Badge text
        color: Badge background color
    """
    st.markdown(
        f"<span style='background-color: {color}; color: white; padding: 0.25rem 0.5rem; border-radius: 0.25rem;'>{text}</span>",
        unsafe_allow_html=True
    )


def render_progress_bar(
    value: float,
    max_value: float = 100.0,
    label: str = ""
) -> None:
    """
    Render a progress bar.
    
    Args:
        value: Current progress value
        max_value: Maximum progress value
        label: Optional label
    """
    if label:
        st.write(label)
    st.progress(min(value / max_value, 1.0))


def render_button_group(buttons: List[Tuple[str, Callable, str]]) -> None:
    """
    Render a group of buttons.
    
    Args:
        buttons: List of (label, callback, key) tuples
    """
    cols = st.columns(len(buttons))
    for col, (label, callback, key) in zip(cols, buttons):
        with col:
            if st.button(label, key=key, use_container_width=True):
                callback()


class FormBuilder:
    """Helper class for building forms"""
    
    def __init__(self):
        self.fields = {}
    
    def add_text_input(self, label: str, key: str, **kwargs) -> None:
        """Add a text input field"""
        self.fields[key] = ("text_input", label, kwargs)
    
    def add_text_area(self, label: str, key: str, **kwargs) -> None:
        """Add a text area field"""
        self.fields[key] = ("text_area", label, kwargs)
    
    def add_selectbox(self, label: str, options: List, key: str, **kwargs) -> None:
        """Add a selectbox field"""
        self.fields[key] = ("selectbox", label, {"options": options, **kwargs})
    
    def add_slider(self, label: str, min_val: float, max_val: float, key: str, **kwargs) -> None:
        """Add a slider field"""
        self.fields[key] = ("slider", label, {"min_value": min_val, "max_value": max_val, **kwargs})
    
    def add_checkbox(self, label: str, key: str, **kwargs) -> None:
        """Add a checkbox field"""
        self.fields[key] = ("checkbox", label, kwargs)
    
    def render(self) -> Dict[str, Any]:
        """Render the form and return values"""
        values = {}
        for key, (field_type, label, kwargs) in self.fields.items():
            if field_type == "text_input":
                values[key] = st.text_input(label, key=key, **kwargs)
            elif field_type == "text_area":
                values[key] = st.text_area(label, key=key, **kwargs)
            elif field_type == "selectbox":
                options = kwargs.pop("options")
                values[key] = st.selectbox(label, options, key=key, **kwargs)
            elif field_type == "slider":
                min_val = kwargs.pop("min_value")
                max_val = kwargs.pop("max_value")
                values[key] = st.slider(label, min_val, max_val, key=key, **kwargs)
            elif field_type == "checkbox":
                values[key] = st.checkbox(label, key=key, **kwargs)
        
        return values
