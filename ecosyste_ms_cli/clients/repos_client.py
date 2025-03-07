"""
Client for interacting with the Ecosyste.ms Repositories API.
"""
import requests
from typing import Dict, List, Optional, Any, Union
import logging

from ..utils.errors import ApiError, TopicNotFoundError


class RepositoriesClient:
    """
    Client for interacting with the Ecosyste.ms Repositories API.
    Provides methods for fetching topics and repositories.
    """
    
    def __init__(self, base_url: str = "https://repos.ecosyste.ms/api/v1"):
        """
        Initialize the client with the base URL.
        
        Args:
            base_url: Base URL for the API
        """
        self.base_url = base_url.rstrip("/")
        self.logger = logging.getLogger("ecosystems")
    
    def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """
        Make a request to the API and handle errors.
        
        Args:
            endpoint: API endpoint to call
            params: Optional parameters to include in the request
            
        Returns:
            Response data as JSON
            
        Raises:
            ApiError: If the API returns an error
            TopicNotFoundError: If a requested topic is not found
        """
        url = f"{self.base_url}/{endpoint}"
        self.logger.debug(f"Making request to {url} with params {params}")
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                if "topics" in endpoint:
                    # Extract topic name from endpoint
                    topic_name = endpoint.split("/")[-1]
                    raise TopicNotFoundError(topic_name)
                else:
                    raise ApiError(f"Resource not found: {endpoint}")
            else:
                raise ApiError(f"API error: {str(e)}")
        except requests.exceptions.RequestException as e:
            raise ApiError(f"Request error: {str(e)}")
        except ValueError as e:
            raise ApiError(f"Invalid JSON response: {str(e)}")
    
    def get_topics(self, page: int = 1, per_page: int = 30) -> List[Dict[str, Any]]:
        """
        Get a list of topics.
        
        Args:
            page: Page number for pagination
            per_page: Number of items per page
            
        Returns:
            List of topics
        """
        params = {
            "page": page,
            "per_page": per_page
        }
        
        return self._make_request("topics", params)
    
    def get_topic(self, topic_name: str) -> Dict[str, Any]:
        """
        Get information about a specific topic including its repositories.
        
        Args:
            topic_name: Name of the topic
            
        Returns:
            Topic data including repositories
            
        Raises:
            TopicNotFoundError: If the topic is not found
        """
        return self._make_request(f"topics/{topic_name}")
    
    def get_repositories_by_topic(self, topic: str, page: int = 1, per_page: int = 30) -> List[Dict[str, Any]]:
        """
        Get a list of repositories for a topic.
        
        Args:
            topic: Topic name
            page: Page number for pagination
            per_page: Number of items per page
            
        Returns:
            List of repositories
            
        Raises:
            TopicNotFoundError: If the topic is not found
        """
        # Get topic data which includes repositories
        topic_data = self.get_topic(topic)
        
        # Extract repositories and paginate manually
        repositories = topic_data.get("repositories", [])
        
        # Calculate slice for pagination
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        
        return repositories[start_idx:end_idx]
    
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        # No resources to clean up
        pass
