"""
Caching utilities for Ecosyste.ms CLI.
"""
import os
import json
import hashlib
import time
from typing import Any, Dict, Optional, Callable, TypeVar, cast
from functools import wraps

T = TypeVar('T')


class Cache:
    """Simple file-based cache for API responses."""
    
    def __init__(self, cache_dir: Optional[str] = None, ttl: int = 3600):
        """
        Initialize cache with directory and TTL.
        
        Args:
            cache_dir: Directory to store cache files (default: ~/.cache/ecosystems)
            ttl: Time-to-live in seconds (default: 1 hour)
        """
        self.cache_dir = cache_dir or os.path.expanduser("~/.cache/ecosystems")
        os.makedirs(self.cache_dir, exist_ok=True)
        self.ttl = ttl
    
    def _get_cache_key(self, key_data: Any) -> str:
        """Generate a cache key from input data."""
        if isinstance(key_data, str):
            serialized = key_data
        else:
            serialized = json.dumps(key_data, sort_keys=True)
        return hashlib.md5(serialized.encode()).hexdigest()
    
    def _get_cache_path(self, key: str) -> str:
        """Get file path for a cache key."""
        return os.path.join(self.cache_dir, f"{key}.json")
    
    def get(self, key_data: Any) -> Optional[Dict[str, Any]]:
        """Get cached data if available and not expired."""
        key = self._get_cache_key(key_data)
        path = self._get_cache_path(key)
        
        if not os.path.exists(path):
            return None
            
        try:
            with open(path, "r") as f:
                cached = json.load(f)
                
            if time.time() - cached["timestamp"] > self.ttl:
                # Cache expired
                return None
                
            return cached["data"]
        except Exception:
            return None
    
    def set(self, key_data: Any, data: Any) -> None:
        """Cache data with timestamp."""
        key = self._get_cache_key(key_data)
        path = self._get_cache_path(key)
        
        try:
            with open(path, "w") as f:
                json.dump({
                    "timestamp": time.time(),
                    "data": data
                }, f)
        except Exception:
            # Fail silently on cache write errors
            pass
    
    def cached(self, func: Callable[..., T]) -> Callable[..., T]:
        """Decorator to cache function results."""
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            # Skip caching if no_cache is in kwargs
            if kwargs.get("no_cache", False):
                if "no_cache" in kwargs:
                    kwargs.pop("no_cache")
                return func(*args, **kwargs)
            
            # Create cache key from function name and arguments
            key_data = {
                "func": func.__name__,
                "args": args,
                "kwargs": {k: v for k, v in kwargs.items() if k != "no_cache"}
            }
            
            cached_result = self.get(key_data)
            if cached_result is not None:
                return cast(T, cached_result)
                
            result = func(*args, **kwargs)
            
            # Only cache dictionaries and lists
            if isinstance(result, (dict, list)):
                self.set(key_data, result)
                
            return result
            
        return wrapper


def get_cache(ttl: int = 3600) -> Cache:
    """Get a cache instance with the specified TTL."""
    if not hasattr(get_cache, "instance"):
        get_cache.instance = Cache(ttl=ttl)  # type: ignore
    return get_cache.instance  # type: ignore
