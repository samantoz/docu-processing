"""Configuration management for Streamlit applications"""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional
import os
from dotenv import load_dotenv


@dataclass
class AppConfig:
    """Application configuration class for Streamlit apps"""
    
    # Basic app settings
    app_name: str = "Streamlit Application"
    app_description: str = "A modular Streamlit application"
    app_icon: str = "🚀"
    
    # Page configuration
    page_config: Dict[str, Any] = field(default_factory=lambda: {
        "layout": "wide",
        "initial_sidebar_state": "expanded",
    })
    
    # Theme settings
    theme: str = "light"
    primary_color: str = "#1f77b4"
    secondary_color: str = "#ff7f0e"
    
    # UI customization
    sidebar_enabled: bool = True
    dark_mode_enabled: bool = True
    
    # Environment variables
    env_file: Optional[str] = None
    env_vars: Dict[str, str] = field(default_factory=dict)
    
    # Logging
    log_level: str = "INFO"
    log_file: Optional[str] = None
    
    # Cache settings
    cache_enabled: bool = True
    cache_ttl: int = 3600  # in seconds
    
    def __post_init__(self):
        """Initialize configuration after dataclass creation"""
        # Load environment variables if env_file is specified
        if self.env_file:
            load_dotenv(self.env_file)
        
        # Update page_config with basic settings
        self.page_config.update({
            "page_title": self.app_name,
            "page_icon": self.app_icon,
        })
    
    @classmethod
    def from_env(cls, env_file: str = ".env") -> "AppConfig":
        """Create AppConfig from environment variables"""
        config = cls(env_file=env_file)
        config.env_vars = {k: v for k, v in os.environ.items()}
        return config
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary"""
        return {
            "app_name": self.app_name,
            "app_description": self.app_description,
            "app_icon": self.app_icon,
            "page_config": self.page_config,
            "theme": self.theme,
            "primary_color": self.primary_color,
            "secondary_color": self.secondary_color,
            "sidebar_enabled": self.sidebar_enabled,
            "dark_mode_enabled": self.dark_mode_enabled,
            "log_level": self.log_level,
        }
    
    def get_env_var(self, key: str, default: str = "") -> str:
        """Get environment variable with fallback to configured vars"""
        return os.getenv(key, self.env_vars.get(key, default))
