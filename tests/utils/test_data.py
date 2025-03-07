"""
Tests for data processing utilities.
"""
import pytest
from ecosyste_ms_cli.utils.data import (
    filter_dict, extract_value, filter_list,
    search_dict, flatten_dict, sort_items
)


class TestFilterDict:
    def test_include_keys(self):
        # Arrange
        data = {"a": 1, "b": 2, "c": 3}
        keys = ["a", "c"]
        
        # Act
        result = filter_dict(data, keys)
        
        # Assert
        assert result == {"a": 1, "c": 3}
    
    def test_nonexistent_keys(self):
        # Arrange
        data = {"a": 1, "b": 2}
        keys = ["a", "z"]
        
        # Act
        result = filter_dict(data, keys)
        
        # Assert
        assert result == {"a": 1}
    
    def test_empty_keys(self):
        # Arrange
        data = {"a": 1, "b": 2}
        keys = []
        
        # Act
        result = filter_dict(data, keys)
        
        # Assert
        assert result == {}


class TestExtractValue:
    def test_simple_path(self):
        # Arrange
        data = {"user": "john"}
        path = "user"
        
        # Act
        result = extract_value(data, path)
        
        # Assert
        assert result == "john"
    
    def test_nested_path(self):
        # Arrange
        data = {"user": {"profile": {"name": "john"}}}
        path = "user.profile.name"
        
        # Act
        result = extract_value(data, path)
        
        # Assert
        assert result == "john"
    
    def test_nonexistent_path(self):
        # Arrange
        data = {"user": {"profile": {"name": "john"}}}
        path = "user.settings.theme"
        
        # Act
        result = extract_value(data, path)
        
        # Assert
        assert result is None
    
    def test_nonexistent_root(self):
        # Arrange
        data = {"user": {"profile": {"name": "john"}}}
        path = "account.name"
        
        # Act
        result = extract_value(data, path)
        
        # Assert
        assert result is None


class TestFilterList:
    def test_filter_numbers(self):
        # Arrange
        items = [1, 2, 3, 4, 5]
        matcher = lambda x: x > 3
        
        # Act
        result = filter_list(items, matcher)
        
        # Assert
        assert result == [4, 5]
    
    def test_filter_dicts(self):
        # Arrange
        items = [
            {"name": "john", "age": 25},
            {"name": "jane", "age": 30},
            {"name": "bob", "age": 20}
        ]
        matcher = lambda x: x["age"] >= 25
        
        # Act
        result = filter_list(items, matcher)
        
        # Assert
        assert result == [
            {"name": "john", "age": 25},
            {"name": "jane", "age": 30}
        ]
    
    def test_filter_empty_list(self):
        # Arrange
        items = []
        matcher = lambda x: True
        
        # Act
        result = filter_list(items, matcher)
        
        # Assert
        assert result == []


class TestSearchDict:
    def test_search_string_value(self):
        # Arrange
        data = {"name": "John Doe", "email": "john@example.com"}
        term = "john"
        
        # Act
        result = search_dict(data, term)
        
        # Assert
        assert result is True
    
    def test_search_case_insensitive(self):
        # Arrange
        data = {"name": "John Doe", "email": "john@example.com"}
        term = "JOHN"
        
        # Act
        result = search_dict(data, term)
        
        # Assert
        assert result is True
    
    def test_search_nested_dict(self):
        # Arrange
        data = {"user": {"name": "John Doe", "email": "john@example.com"}}
        term = "john"
        
        # Act
        result = search_dict(data, term)
        
        # Assert
        assert result is True
    
    def test_search_in_list(self):
        # Arrange
        data = {"tags": [{"name": "python"}, {"name": "javascript"}]}
        term = "python"
        
        # Act
        result = search_dict(data, term)
        
        # Assert
        assert result is True
    
    def test_search_not_found(self):
        # Arrange
        data = {"name": "John Doe", "email": "john@example.com"}
        term = "ruby"
        
        # Act
        result = search_dict(data, term)
        
        # Assert
        assert result is False


class TestFlattenDict:
    def test_simple_dict(self):
        # Arrange
        data = {"a": 1, "b": 2}
        
        # Act
        result = flatten_dict(data)
        
        # Assert
        assert result == {"a": 1, "b": 2}
    
    def test_nested_dict(self):
        # Arrange
        data = {"user": {"name": "John", "age": 30}}
        
        # Act
        result = flatten_dict(data)
        
        # Assert
        assert result == {"user.name": "John", "user.age": 30}
    
    def test_deeply_nested_dict(self):
        # Arrange
        data = {"user": {"profile": {"name": "John", "contact": {"email": "john@example.com"}}}}
        
        # Act
        result = flatten_dict(data)
        
        # Assert
        assert result == {
            "user.profile.name": "John",
            "user.profile.contact.email": "john@example.com"
        }
    
    def test_empty_dict(self):
        # Arrange
        data = {}
        
        # Act
        result = flatten_dict(data)
        
        # Assert
        assert result == {}


class TestSortItems:
    def test_sort_by_simple_key_ascending(self):
        # Arrange
        items = [
            {"name": "B", "count": 5},
            {"name": "A", "count": 10},
            {"name": "C", "count": 2}
        ]
        
        # Act
        result = sort_items(items, "name", "asc")
        
        # Assert
        assert result[0]["name"] == "A"
    
    def test_sort_by_simple_key_descending(self):
        # Arrange
        items = [
            {"name": "B", "count": 5},
            {"name": "A", "count": 10},
            {"name": "C", "count": 2}
        ]
        
        # Act
        result = sort_items(items, "count", "desc")
        
        # Assert
        assert result[0]["count"] == 10
    
    def test_sort_by_nested_key(self):
        # Arrange
        items = [
            {"name": "B", "stats": {"stars": 50}},
            {"name": "A", "stats": {"stars": 100}},
            {"name": "C", "stats": {"stars": 20}}
        ]
        
        # Act
        result = sort_items(items, "stats.stars", "desc")
        
        # Assert
        assert result[0]["name"] == "A"  # 100 stars
    
    def test_sort_with_missing_keys(self):
        # Arrange
        items = [
            {"name": "B", "count": 5},
            {"name": "A"},  # missing count
            {"name": "C", "count": 2}
        ]
        
        # Act
        result = sort_items(items, "count", "desc")
        
        # Assert
        assert result[0]["count"] == 5
    
    def test_sort_empty_list(self):
        # Arrange
        items = []
        
        # Act
        result = sort_items(items, "name", "asc")
        
        # Assert
        assert result == []
