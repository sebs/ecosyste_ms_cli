"""
Tests for output formatting utilities.
"""
import pytest
import json
from ecosyste_ms_cli.commands.common import OutputFormat
from ecosyste_ms_cli.utils.output import format_output, format_table, truncate_string


class TestFormatOutput:
    def test_json_formatting_single_item(self):
        # Arrange
        data = {"name": "test", "value": 123}
        
        # Act
        result = format_output(data, OutputFormat.JSON)
        
        # Assert
        assert json.loads(result) == data
    
    def test_json_formatting_multiple_items(self):
        # Arrange
        data = [
            {"name": "test1", "value": 123},
            {"name": "test2", "value": 456}
        ]
        
        # Act
        result = format_output(data, OutputFormat.JSON)
        
        # Assert
        assert json.loads(result) == data
    
    def test_csv_formatting(self):
        # Arrange
        data = [
            {"name": "test1", "value": 123},
            {"name": "test2", "value": 456}
        ]
        
        # Act
        result = format_output(data, OutputFormat.CSV)
        
        # Assert
        assert "name,value" in result
        assert "test1,123" in result
        assert "test2,456" in result
    
    def test_tsv_formatting(self):
        # Arrange
        data = [
            {"name": "test1", "value": 123},
            {"name": "test2", "value": 456}
        ]
        
        # Act
        result = format_output(data, OutputFormat.TSV)
        
        # Assert
        assert "name\tvalue" in result
        assert "test1\t123" in result
        assert "test2\t456" in result
    
    def test_empty_list(self):
        # Arrange
        data = []
        
        # Act
        result = format_output(data, OutputFormat.CSV)
        
        # Assert
        assert result == ""


class TestFormatTable:
    def test_table_formatting(self):
        # Arrange
        data = [
            {"name": "test1", "value": 123},
            {"name": "test2", "value": 456}
        ]
        
        # Act
        result = format_table(data)
        
        # Assert
        assert "name" in result
        assert "value" in result
        assert "test1" in result
        assert "test2" in result
    
    def test_table_with_custom_headers(self):
        # Arrange
        data = [
            ["test1", 123],
            ["test2", 456]
        ]
        headers = ["Name", "Value"]
        
        # Act
        result = format_table(data, headers=headers)
        
        # Assert
        assert "Name" in result
        assert "Value" in result


class TestTruncateString:
    def test_truncate_long_string(self):
        # Arrange
        test_string = "a" * 100
        max_length = 50
        
        # Act
        result = truncate_string(test_string, max_length)
        
        # Assert
        assert len(result) == max_length
        assert result.endswith("...")
    
    def test_not_truncate_short_string(self):
        # Arrange
        test_string = "short string"
        max_length = 50
        
        # Act
        result = truncate_string(test_string, max_length)
        
        # Assert
        assert result == test_string
