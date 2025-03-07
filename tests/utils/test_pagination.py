"""
Tests for pagination utilities.
"""
import pytest
from typing import List, Dict, Any
from ecosyste_ms_cli.utils.pagination import paginate, collect_pages


class TestPagination:
    def test_paginate_single_page(self):
        # Arrange
        items = [{"id": 1}, {"id": 2}, {"id": 3}]
        
        def mock_fetch(page, per_page):
            if page == 1:
                return items
            return []
            
        # Act
        results = list(paginate(mock_fetch, page=1, per_page=10))
        
        # Assert
        assert results == items
    
    def test_paginate_multiple_pages(self):
        # Arrange
        page1 = [{"id": 1}, {"id": 2}]
        page2 = [{"id": 3}, {"id": 4}]
        page3 = []
        
        def mock_fetch(page, per_page):
            if page == 1:
                return page1
            elif page == 2:
                return page2
            else:
                return page3
            
        # Act
        results = list(paginate(mock_fetch, page=1, per_page=2))
        
        # Assert
        assert results == page1 + page2
    
    def test_paginate_max_items(self):
        # Arrange
        page1 = [{"id": 1}, {"id": 2}]
        page2 = [{"id": 3}, {"id": 4}]
        
        def mock_fetch(page, per_page):
            if page == 1:
                return page1
            elif page == 2:
                return page2
            else:
                return []
            
        # Act
        results = list(paginate(mock_fetch, page=1, per_page=2, max_items=3))
        
        # Assert
        assert len(results) == 3
    
    def test_paginate_custom_start_page(self):
        # Arrange
        page2 = [{"id": 3}, {"id": 4}]
        
        def mock_fetch(page, per_page):
            if page == 2:
                return page2
            return []
            
        # Act
        results = list(paginate(mock_fetch, page=2, per_page=2))
        
        # Assert
        assert results == page2


class TestCollectPages:
    def test_collect_pages_single_page(self):
        # Arrange
        items = [{"id": 1}, {"id": 2}, {"id": 3}]
        
        def mock_fetch(page, per_page):
            if page == 1:
                return items
            return []
            
        # Act
        results = collect_pages(mock_fetch, page=1, per_page=10)
        
        # Assert
        assert results == items
    
    def test_collect_pages_multiple_pages(self):
        # Arrange
        page1 = [{"id": 1}, {"id": 2}]
        page2 = [{"id": 3}, {"id": 4}]
        
        def mock_fetch(page, per_page):
            if page == 1:
                return page1
            elif page == 2:
                return page2
            else:
                return []
            
        # Act
        results = collect_pages(mock_fetch, page=1, per_page=2)
        
        # Assert
        assert results == page1 + page2
    
    def test_collect_pages_max_pages(self):
        # Arrange
        page1 = [{"id": 1}, {"id": 2}]
        page2 = [{"id": 3}, {"id": 4}]
        page3 = [{"id": 5}, {"id": 6}]
        
        def mock_fetch(page, per_page):
            if page == 1:
                return page1
            elif page == 2:
                return page2
            elif page == 3:
                return page3
            else:
                return []
            
        # Act
        results = collect_pages(mock_fetch, page=1, per_page=2, max_pages=2)
        
        # Assert
        assert results == page1 + page2
