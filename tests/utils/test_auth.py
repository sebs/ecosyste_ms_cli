"""
Tests for authentication utilities.
"""
import pytest
import os
import json
import tempfile
from unittest.mock import patch, mock_open
from ecosyste_ms_cli.utils.auth import AuthManager, get_auth_manager


class TestAuthManager:
    def test_init_creates_config_dir(self):
        # Arrange
        with tempfile.TemporaryDirectory() as temp_dir:
            config_dir = os.path.join(temp_dir, "config")
            
            # Act
            auth_manager = AuthManager(config_dir=config_dir)
            
            # Assert
            assert os.path.exists(config_dir)
    
    def test_set_api_key(self):
        # Arrange
        with tempfile.TemporaryDirectory() as temp_dir:
            config_dir = os.path.join(temp_dir, "config")
            auth_manager = AuthManager(config_dir=config_dir)
            service = "test_service"
            api_key = "test_api_key"
            
            # Act
            with patch("builtins.open", mock_open()) as mock_file:
                auth_manager.set_api_key(service, api_key)
            
            # Assert
            assert auth_manager._credentials[service]["api_key"] == api_key
    
    def test_get_api_key_exists(self):
        # Arrange
        with tempfile.TemporaryDirectory() as temp_dir:
            config_dir = os.path.join(temp_dir, "config")
            auth_manager = AuthManager(config_dir=config_dir)
            service = "test_service"
            api_key = "test_api_key"
            auth_manager._credentials = {service: {"api_key": api_key}}
            
            # Act
            result = auth_manager.get_api_key(service)
            
            # Assert
            assert result == api_key
    
    def test_get_api_key_not_exists(self):
        # Arrange
        with tempfile.TemporaryDirectory() as temp_dir:
            config_dir = os.path.join(temp_dir, "config")
            auth_manager = AuthManager(config_dir=config_dir)
            service = "nonexistent_service"
            
            # Act
            result = auth_manager.get_api_key(service)
            
            # Assert
            assert result is None
    
    def test_get_headers_with_api_key(self):
        # Arrange
        with tempfile.TemporaryDirectory() as temp_dir:
            config_dir = os.path.join(temp_dir, "config")
            auth_manager = AuthManager(config_dir=config_dir)
            service = "test_service"
            api_key = "test_api_key"
            auth_manager._credentials = {service: {"api_key": api_key}}
            
            # Act
            headers = auth_manager.get_headers(service)
            
            # Assert
            assert headers["Authorization"] == f"Bearer {api_key}"
    
    def test_get_headers_without_api_key(self):
        # Arrange
        with tempfile.TemporaryDirectory() as temp_dir:
            config_dir = os.path.join(temp_dir, "config")
            auth_manager = AuthManager(config_dir=config_dir)
            service = "nonexistent_service"
            
            # Act
            headers = auth_manager.get_headers(service)
            
            # Assert
            assert headers == {}
    
    def test_load_credentials(self):
        # Arrange
        with tempfile.TemporaryDirectory() as temp_dir:
            config_dir = os.path.join(temp_dir, "config")
            os.makedirs(config_dir, exist_ok=True)
            config_file = os.path.join(config_dir, "auth.json")
            credentials = {"test_service": {"api_key": "test_api_key"}}
            
            with open(config_file, "w") as f:
                json.dump(credentials, f)
                
            # Act
            auth_manager = AuthManager(config_dir=config_dir)
            
            # Assert
            assert auth_manager._credentials == credentials


class TestGetAuthManager:
    def test_get_auth_manager_singleton(self):
        # Arrange & Act
        auth_manager1 = get_auth_manager()
        auth_manager2 = get_auth_manager()
        
        # Assert
        assert auth_manager1 is auth_manager2
