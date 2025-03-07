"""
Authentication utilities for Ecosyste.ms CLI.
"""
import os
import json
from typing import Optional, Dict, Any

import typer


class AuthManager:
    """Manager for API authentication."""
    
    def __init__(self, config_dir: Optional[str] = None):
        """Initialize with optional config directory."""
        self.config_dir = config_dir or os.path.expanduser("~/.config/ecosystems")
        os.makedirs(self.config_dir, exist_ok=True)
        self.config_file = os.path.join(self.config_dir, "auth.json")
        self._credentials = {}
        self._load_credentials()
    
    def _load_credentials(self) -> None:
        """Load credentials from config file."""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, "r") as f:
                    self._credentials = json.load(f)
        except Exception as e:
            typer.echo(f"Error loading credentials: {str(e)}", err=True)
    
    def _save_credentials(self) -> None:
        """Save credentials to config file."""
        try:
            with open(self.config_file, "w") as f:
                json.dump(self._credentials, f)
        except Exception as e:
            typer.echo(f"Error saving credentials: {str(e)}", err=True)
    
    def set_api_key(self, service: str, api_key: str) -> None:
        """Set API key for a service."""
        self._credentials[service] = {"api_key": api_key}
        self._save_credentials()
    
    def get_api_key(self, service: str) -> Optional[str]:
        """Get API key for a service."""
        service_creds = self._credentials.get(service, {})
        return service_creds.get("api_key")
    
    def get_headers(self, service: str) -> Dict[str, str]:
        """Get authentication headers for API requests."""
        api_key = self.get_api_key(service)
        if api_key:
            return {"Authorization": f"Bearer {api_key}"}
        return {}


def get_auth_manager() -> AuthManager:
    """Get a singleton instance of AuthManager."""
    if not hasattr(get_auth_manager, "instance"):
        get_auth_manager.instance = AuthManager()  # type: ignore
    return get_auth_manager.instance  # type: ignore
