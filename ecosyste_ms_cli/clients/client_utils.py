"""
Client utility classes for working with the generated API clients.
"""
from typing import Any, Dict, List, Optional, Type, TypeVar, Generic

T = TypeVar('T')


class BaseClientWrapper(Generic[T]):
    """
    Base class for API client wrappers that provides common functionality.
    
    This class follows the principle of keeping the API explicit and readable
    while abstracting away some of the complexity of the generated clients.
    """
    
    def __init__(self, api_client_class: Type[T], base_url: Optional[str] = None):
        """
        Initialize a client wrapper.
        
        Args:
            api_client_class: The generated API client class to wrap
            base_url: Optional custom base URL for the API
        """
        # Create configuration with custom base URL if provided
        if base_url:
            # We'll use a more generic approach to avoid direct imports
            # This will be configured properly when the actual clients are available
            configuration = None
            try:
                # Try to import the configuration class dynamically
                module_name = api_client_class.__module__.rsplit('.', 1)[0]
                config_module = __import__(f"{module_name}.configuration", fromlist=['Configuration'])
                configuration = config_module.Configuration()
                configuration.host = base_url
            except (ImportError, AttributeError):
                # If import fails, we'll set up a basic configuration
                configuration = {'host': base_url}
                
            self.api_client = api_client_class(configuration=configuration)
        else:
            self.api_client = api_client_class()
    
    def handle_pagination(self, method: callable, *args, **kwargs) -> List[Dict[str, Any]]:
        """
        Handle pagination for API calls that support it.
        
        Args:
            method: The API method to call
            *args: Positional arguments to pass to the method
            **kwargs: Keyword arguments to pass to the method
            
        Returns:
            A list of all results across all pages
        """
        page = 1
        per_page = kwargs.get('per_page', 30)
        all_results = []
        
        while True:
            # Update page parameter
            kwargs['page'] = page
            
            # Make the API call
            results = method(*args, **kwargs)
            
            # If results is empty or not a list, stop pagination
            if not results or not isinstance(results, list):
                break
                
            all_results.extend(results)
            
            # If we got fewer results than requested per page, we're done
            if len(results) < per_page:
                break
                
            # Move to the next page
            page += 1
            
        return all_results
