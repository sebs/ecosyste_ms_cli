"""
Repository API client stub for Ecosyste.ms CLI.
This is a stub implementation that returns mock data for development and testing.
"""
import sys
import os
import time
from typing import List, Dict, Any, Optional

from ecosyste_ms_cli.utils.errors import TopicNotFoundError, RepositoryNotFoundError, APIError


class Repositories:
    """Wrapper for the Ecosyste.ms Repositories API client.
    
    Provides methods for accessing repository metadata, topics, and other
    Ecosyste.ms Repositories API functionality.
    """
    
    def __init__(self, api_url: Optional[str] = None):
        """Initialize the repositories API client stub.
        
        Args:
            api_url: Ignored in stub implementation
        """
        # Stub data for development and testing
        self._stub_topics = [
            {"name": "python", "repositories_count": 100},
            {"name": "javascript", "repositories_count": 150},
            {"name": "ruby", "repositories_count": 75},
            {"name": "rust", "repositories_count": 50},
            {"name": "go", "repositories_count": 120}
        ]
        
        self._stub_repos = {
            "python": [
                {"name": "django", "full_name": "django/django", "stars": 1000, "forks": 500, "description": "The Web framework for perfectionists with deadlines."},
                {"name": "flask", "full_name": "pallets/flask", "stars": 800, "forks": 400, "description": "The Python micro framework for building web applications."},
                {"name": "fastapi", "full_name": "tiangolo/fastapi", "stars": 600, "forks": 300, "description": "FastAPI framework, high performance, easy to learn, fast to code, ready for production."}
            ],
            "javascript": [
                {"name": "react", "full_name": "facebook/react", "stars": 1500, "forks": 700, "description": "A declarative, efficient, and flexible JavaScript library for building user interfaces."},
                {"name": "vue", "full_name": "vuejs/vue", "stars": 1300, "forks": 650, "description": "Vue.js is a progressive, incrementally-adoptable JavaScript framework for building UI on the web."},
                {"name": "angular", "full_name": "angular/angular", "stars": 1100, "forks": 550, "description": "One framework. Mobile & desktop."}
            ]
        }
        
    def __enter__(self):
        """Context manager entry point"""
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit point"""
        pass

    def _simulate_latency(self):
        """Simulate network latency for more realistic testing."""
        time.sleep(0.1)  # 100ms delay

    def get_topics(self, page: int = 1, per_page: int = 30) -> List[Dict[str, Any]]:
        """Get a list of topics (stub implementation).
        
        Args:
            page: Page number
            per_page: Number of items per page
            
        Returns:
            List of topics
        """
        self._simulate_latency()
        
        # Apply pagination to stub data
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        return self._stub_topics[start_idx:end_idx]
            
    def get_topic(self, topic_name: str) -> Dict[str, Any]:
        """Get a specific topic with its repositories (stub implementation).
        
        Args:
            topic_name: Name of the topic
            
        Returns:
            Topic information with repositories
            
        Raises:
            TopicNotFoundError: If the topic does not exist
        """
        self._simulate_latency()
        
        # Check if topic exists in stub data
        for topic in self._stub_topics:
            if topic["name"] == topic_name:
                repositories = self._stub_repos.get(topic_name, [])
                return {
                    "name": topic_name,
                    "repositories_count": len(repositories),
                    "repositories": repositories
                }
        
        # Topic not found
        raise TopicNotFoundError(topic_name)
            
    def get_repositories_by_topic(
        self, 
        topic: str, 
        page: int = 1, 
        per_page: int = 30
    ) -> List[Dict[str, Any]]:
        """Get repositories for a specific topic (stub implementation).
        
        Args:
            topic: Topic name
            page: Page number
            per_page: Number of items per page
            
        Returns:
            List of repositories
            
        Raises:
            TopicNotFoundError: If the topic does not exist
        """
        self._simulate_latency()
        
        # Check if topic exists in stub data
        if topic in self._stub_repos:
            repositories = self._stub_repos[topic]
            # Apply pagination
            start_idx = (page - 1) * per_page
            end_idx = start_idx + per_page
            return repositories[start_idx:end_idx]
        
        # Topic not found
        raise TopicNotFoundError(topic)
