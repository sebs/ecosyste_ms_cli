"""
Logging utilities for Ecosyste.ms CLI.
"""
import logging
import os
import sys
from typing import Optional, Union, TextIO


class CLILogger:
    """Configurable logger for CLI operations."""
    
    DEFAULT_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    def __init__(
        self,
        name: str = "ecosystems",
        level: int = logging.INFO,
        log_file: Optional[str] = None,
        verbose: bool = False
    ):
        """
        Initialize logger with name and level.
        
        Args:
            name: Logger name
            level: Logging level (default: INFO)
            log_file: Optional file to log to
            verbose: Enable verbose logging (sets level to DEBUG)
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG if verbose else level)
        self.logger.handlers = []  # Clear existing handlers
        
        # Console handler
        console = logging.StreamHandler(sys.stderr)
        console.setLevel(logging.DEBUG if verbose else level)
        formatter = logging.Formatter(self.DEFAULT_FORMAT)
        console.setFormatter(formatter)
        self.logger.addHandler(console)
        
        # File handler if specified
        if log_file:
            log_dir = os.path.dirname(os.path.abspath(log_file))
            os.makedirs(log_dir, exist_ok=True)
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.DEBUG)  # Always debug to file
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
    
    def debug(self, msg: str) -> None:
        """Log a debug message."""
        self.logger.debug(msg)
    
    def info(self, msg: str) -> None:
        """Log an info message."""
        self.logger.info(msg)
    
    def warning(self, msg: str) -> None:
        """Log a warning message."""
        self.logger.warning(msg)
    
    def error(self, msg: str) -> None:
        """Log an error message."""
        self.logger.error(msg)
    
    def critical(self, msg: str) -> None:
        """Log a critical message."""
        self.logger.critical(msg)


def get_logger(
    name: str = "ecosystems",
    verbose: bool = False,
    log_file: Optional[str] = None
) -> CLILogger:
    """
    Get a configured logger instance.
    
    Args:
        name: Logger name
        verbose: Enable verbose logging
        log_file: Optional file to log to
        
    Returns:
        Configured CLILogger instance
    """
    return CLILogger(name, verbose=verbose, log_file=log_file)
