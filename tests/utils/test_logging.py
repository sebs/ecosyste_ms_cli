"""
Tests for logging utilities.
"""
import pytest
import logging
import os
import tempfile
from unittest.mock import patch, MagicMock
from ecosyste_ms_cli.utils.logging import CLILogger, get_logger


class TestCLILogger:
    def test_init_default(self):
        # Arrange & Act
        logger = CLILogger()
        
        # Assert
        assert logger.logger.level == logging.INFO
        assert len(logger.logger.handlers) == 1
        assert isinstance(logger.logger.handlers[0], logging.StreamHandler)
    
    def test_init_verbose(self):
        # Arrange & Act
        logger = CLILogger(verbose=True)
        
        # Assert
        assert logger.logger.level == logging.DEBUG
        assert len(logger.logger.handlers) == 1
    
    def test_init_with_file(self):
        # Arrange
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = os.path.join(temp_dir, "test.log")
            
            # Act
            logger = CLILogger(log_file=log_file)
            
            # Assert
            assert len(logger.logger.handlers) == 2
            assert isinstance(logger.logger.handlers[1], logging.FileHandler)
    
    def test_debug_method(self):
        # Arrange
        with patch('logging.Logger.debug') as mock_debug:
            logger = CLILogger()
            message = "Debug message"
            
            # Act
            logger.debug(message)
            
            # Assert
            mock_debug.assert_called_once_with(message)
    
    def test_info_method(self):
        # Arrange
        with patch('logging.Logger.info') as mock_info:
            logger = CLILogger()
            message = "Info message"
            
            # Act
            logger.info(message)
            
            # Assert
            mock_info.assert_called_once_with(message)
    
    def test_warning_method(self):
        # Arrange
        with patch('logging.Logger.warning') as mock_warning:
            logger = CLILogger()
            message = "Warning message"
            
            # Act
            logger.warning(message)
            
            # Assert
            mock_warning.assert_called_once_with(message)
    
    def test_error_method(self):
        # Arrange
        with patch('logging.Logger.error') as mock_error:
            logger = CLILogger()
            message = "Error message"
            
            # Act
            logger.error(message)
            
            # Assert
            mock_error.assert_called_once_with(message)
    
    def test_critical_method(self):
        # Arrange
        with patch('logging.Logger.critical') as mock_critical:
            logger = CLILogger()
            message = "Critical message"
            
            # Act
            logger.critical(message)
            
            # Assert
            mock_critical.assert_called_once_with(message)


class TestGetLogger:
    def test_get_logger_default(self):
        # Arrange & Act
        logger = get_logger()
        
        # Assert
        assert isinstance(logger, CLILogger)
    
    def test_get_logger_with_name(self):
        # Arrange & Act
        logger = get_logger(name="test_logger")
        
        # Assert
        assert logger.logger.name == "test_logger"
    
    def test_get_logger_verbose(self):
        # Arrange & Act
        logger = get_logger(verbose=True)
        
        # Assert
        assert logger.logger.level == logging.DEBUG
