"""State management utilities for Streamlit"""

import streamlit as st
from typing import Any, Dict, Optional, List


class SessionState:
    """Helper class for managing Streamlit session state"""
    
    @staticmethod
    def set(key: str, value: Any) -> None:
        """Set a session state value"""
        st.session_state[key] = value
    
    @staticmethod
    def get(key: str, default: Any = None) -> Any:
        """Get a session state value"""
        return st.session_state.get(key, default)
    
    @staticmethod
    def exists(key: str) -> bool:
        """Check if a key exists in session state"""
        return key in st.session_state
    
    @staticmethod
    def delete(key: str) -> None:
        """Delete a session state value"""
        if key in st.session_state:
            del st.session_state[key]
    
    @staticmethod
    def clear() -> None:
        """Clear all session state"""
        st.session_state.clear()
    
    @staticmethod
    def get_all() -> Dict[str, Any]:
        """Get all session state values"""
        return dict(st.session_state)


class StateManager:
    """Advanced state management for complex applications"""
    
    def __init__(self, namespace: str = "app"):
        """
        Initialize state manager.
        
        Args:
            namespace: Namespace for state isolation
        """
        self.namespace = namespace
        self._ensure_namespace()
    
    def _ensure_namespace(self) -> None:
        """Ensure namespace exists in session state"""
        if self.namespace not in st.session_state:
            st.session_state[self.namespace] = {}
    
    def set(self, key: str, value: Any) -> None:
        """Set a value in the namespace"""
        self._ensure_namespace()
        st.session_state[self.namespace][key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a value from the namespace"""
        self._ensure_namespace()
        return st.session_state[self.namespace].get(key, default)
    
    def delete(self, key: str) -> None:
        """Delete a value from the namespace"""
        self._ensure_namespace()
        if key in st.session_state[self.namespace]:
            del st.session_state[self.namespace][key]
    
    def clear(self) -> None:
        """Clear all values in the namespace"""
        st.session_state[self.namespace] = {}
    
    def get_all(self) -> Dict[str, Any]:
        """Get all values in the namespace"""
        self._ensure_namespace()
        return st.session_state[self.namespace].copy()
