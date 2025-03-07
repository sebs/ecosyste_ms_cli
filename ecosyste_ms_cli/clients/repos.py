"""
Repository API client wrapper for Ecosyste.ms CLI.
"""
from typing import List, Dict, Any, Optional

from ecosyste_ms_cli.clients.repos.api.default_api import DefaultApi
from ecosyste_ms_cli.clients.repos.models import Topic, Repository
from ecosyste_ms_cli.utils.errors import TopicNotFoundError, RepositoryNotFoundError


class Repositories:
    """Wrapper for the Ecosyste.ms Repositories API client."""
    
    def __init__(self, api_url: Optional[str] = None):
        """Initialize the repositories API client.
        
        Args:
            api_url: Optional override for the API URL
        """
        self.api_url = api_url or "https://repos.ecosyste.ms/api/v1"
        self.client = None
        
    def __enter__(self):
        """Context manager entry point"""
        self.client = DefaultApi()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit point"""
        self.client = None

    def get_topics(self, page: int = 1, per_page: int = 30) -> List[Dict[str, Any]]:
        """Get a list of topics.
        
        Args:
            page: Page number
            per_page: Number of items per page
            
        Returns:
            List of topics
            
        Raises:
            APIError: If the API request fails
        """
        try:
            topics = self.client.topics(page=page, per_page=per_page)
            # Convert API models to dictionaries for consistency
            return [t.to_dict() for t in topics]
        except Exception as e:
            if "404" in str(e):
                return []
            raise e
            
    def get_topic(self, topic_name: str) -> Dict[str, Any]:
        """Get a specific topic with its repositories.
        
        Args:
            topic_name: Name of the topic
            
        Returns:
            Topic information with repositories
            
        Raises:
            TopicNotFoundError: If the topic does not exist
        """
        try:
            topic = self.client.topic(topic=topic_name)
            return topic.to_dict()
        except Exception as e:
            if "404" in str(e):
                raise TopicNotFoundError(topic_name)
            raise e
            
    def get_repositories_by_topic(
        self, 
        topic: str, 
        page: int = 1, 
        per_page: int = 30
    ) -> List[Dict[str, Any]]:
        """Get repositories for a specific topic.
        
        Args:
            topic: Topic name
            page: Page number
            per_page: Number of items per page
            
        Returns:
            List of repositories
            
        Raises:
            TopicNotFoundError: If the topic does not exist
        """
        try:
            topic_data = self.get_topic(topic)
            repositories = topic_data.get("repositories", [])
            # Apply pagination manually since the API doesn't support it for repositories within a topic
            start_idx = (page - 1) * per_page
            end_idx = start_idx + per_page
            return repositories[start_idx:end_idx]
        except TopicNotFoundError:
            raise
        except Exception as e:
            raise e
