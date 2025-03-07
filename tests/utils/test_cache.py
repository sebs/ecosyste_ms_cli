"""
Tests for caching utilities.
"""
import pytest
import os
import json
import tempfile
import time
from unittest.mock import patch, mock_open, MagicMock
from ecosyste_ms_cli.utils.cache import Cache, get_cache


class TestCache:
    def test_init_creates_cache_dir(self):
        # Arrange
        with tempfile.TemporaryDirectory() as temp_dir:
            cache_dir = os.path.join(temp_dir, "cache")
            
            # Act
            cache = Cache(cache_dir=cache_dir)
            
            # Assert
            assert os.path.exists(cache_dir)
    
    def test_get_cache_key_string(self):
        # Arrange
        cache = Cache()
        key_data = "test_key"
        
        # Act
        key = cache._get_cache_key(key_data)
        
        # Assert
        assert isinstance(key, str)
        assert len(key) == 32  # MD5 hash length
    
    def test_get_cache_key_dict(self):
        # Arrange
        cache = Cache()
        key_data = {"test": "value"}
        
        # Act
        key = cache._get_cache_key(key_data)
        
        # Assert
        assert isinstance(key, str)
        assert len(key) == 32  # MD5 hash length
    
    def test_get_cache_path(self):
        # Arrange
        with tempfile.TemporaryDirectory() as temp_dir:
            cache = Cache(cache_dir=temp_dir)
            key = "test_key"
            
            # Act
            path = cache._get_cache_path(key)
            
            # Assert
            assert path == os.path.join(temp_dir, f"{key}.json")
    
    def test_get_nonexistent_cache(self):
        # Arrange
        with tempfile.TemporaryDirectory() as temp_dir:
            cache = Cache(cache_dir=temp_dir)
            key_data = "nonexistent_key"
            
            # Act
            result = cache.get(key_data)
            
            # Assert
            assert result is None
    
    def test_get_expired_cache(self):
        # Arrange
        with tempfile.TemporaryDirectory() as temp_dir:
            cache = Cache(cache_dir=temp_dir, ttl=1)
            key_data = "test_key"
            key = cache._get_cache_key(key_data)
            path = cache._get_cache_path(key)
            
            # Write expired cache file
            expired_data = {
                "timestamp": time.time() - 10,  # 10 seconds ago
                "data": {"test": "value"}
            }
            os.makedirs(temp_dir, exist_ok=True)
            with open(path, "w") as f:
                json.dump(expired_data, f)
            
            # Act
            result = cache.get(key_data)
            
            # Assert
            assert result is None
    
    def test_get_valid_cache(self):
        # Arrange
        with tempfile.TemporaryDirectory() as temp_dir:
            cache = Cache(cache_dir=temp_dir, ttl=3600)
            key_data = "test_key"
            key = cache._get_cache_key(key_data)
            path = cache._get_cache_path(key)
            test_data = {"test": "value"}
            
            # Write valid cache file
            valid_data = {
                "timestamp": time.time(),
                "data": test_data
            }
            os.makedirs(temp_dir, exist_ok=True)
            with open(path, "w") as f:
                json.dump(valid_data, f)
            
            # Act
            result = cache.get(key_data)
            
            # Assert
            assert result == test_data
    
    def test_set_cache(self):
        # Arrange
        with tempfile.TemporaryDirectory() as temp_dir:
            cache = Cache(cache_dir=temp_dir)
            key_data = "test_key"
            test_data = {"test": "value"}
            
            # Act
            with patch("builtins.open", mock_open()) as mock_file:
                cache.set(key_data, test_data)
            
            # Assert
            mock_file.assert_called_once()
    
    def test_cached_decorator_hit(self):
        # Arrange
        with tempfile.TemporaryDirectory() as temp_dir:
            cache = Cache(cache_dir=temp_dir)
            test_data = {"test": "value"}
            
            # Create a mock function
            mock_func = MagicMock(return_value=test_data)
            mock_func.__name__ = "mock_func"
            
            # Create cache key and add to cache
            key_data = {
                "func": "mock_func",
                "args": (),
                "kwargs": {}
            }
            key = cache._get_cache_key(key_data)
            path = cache._get_cache_path(key)
            
            # Write valid cache file
            valid_data = {
                "timestamp": time.time(),
                "data": test_data
            }
            os.makedirs(temp_dir, exist_ok=True)
            with open(path, "w") as f:
                json.dump(valid_data, f)
            
            # Decorate the function
            decorated_func = cache.cached(mock_func)
            
            # Act
            result = decorated_func()
            
            # Assert
            assert result == test_data
            mock_func.assert_not_called()  # Function should not be called when cache hit
    
    def test_cached_decorator_miss(self):
        # Arrange
        with tempfile.TemporaryDirectory() as temp_dir:
            cache = Cache(cache_dir=temp_dir)
            test_data = {"test": "value"}
            
            # Create a mock function
            mock_func = MagicMock(return_value=test_data)
            mock_func.__name__ = "mock_func"
            
            # Decorate the function
            decorated_func = cache.cached(mock_func)
            
            # Act
            with patch.object(cache, "set") as mock_set:
                result = decorated_func()
            
            # Assert
            assert result == test_data
            mock_func.assert_called_once()  # Function should be called on cache miss
            mock_set.assert_called_once()  # Cache set should be called
    
    def test_cached_decorator_no_cache_flag(self):
        # Arrange
        with tempfile.TemporaryDirectory() as temp_dir:
            cache = Cache(cache_dir=temp_dir)
            test_data = {"test": "value"}
            
            # Create a mock function
            mock_func = MagicMock(return_value=test_data)
            mock_func.__name__ = "mock_func"
            
            # Add a mock to cache to confirm we don't use it
            key_data = {
                "func": "mock_func",
                "args": (),
                "kwargs": {}
            }
            key = cache._get_cache_key(key_data)
            path = cache._get_cache_path(key)
            
            # Write valid cache file
            valid_data = {
                "timestamp": time.time(),
                "data": {"cached": "data"}
            }
            os.makedirs(temp_dir, exist_ok=True)
            with open(path, "w") as f:
                json.dump(valid_data, f)
            
            # Decorate the function
            decorated_func = cache.cached(mock_func)
            
            # Act
            with patch.object(cache, "set") as mock_set:
                result = decorated_func(no_cache=True)
            
            # Assert
            assert result == test_data
            mock_func.assert_called_once()  # Function should be called
            mock_set.assert_not_called()  # Cache set should not be called


class TestGetCache:
    def test_get_cache_singleton(self):
        # Arrange & Act
        cache1 = get_cache()
        cache2 = get_cache()
        
        # Assert
        assert cache1 is cache2
    
    def test_get_cache_with_custom_ttl(self):
        # Arrange
        # Clear the singleton instance if it exists
        if hasattr(get_cache, "instance"):
            delattr(get_cache, "instance")
            
        # Act
        cache = get_cache(ttl=7200)
        
        # Assert
        assert cache.ttl == 7200
        
        # Clean up - reset the singleton for other tests
        delattr(get_cache, "instance")
