"""
Configuration for the Repositories API client.
"""

class Configuration:
    """API client configuration."""
    
    def __init__(self, host=None):
        """Initialize configuration with host URL."""
        self.host = host
