"""
MockConfig module for Credit Agricole Particuliers API.

This module provides configuration for mocking API requests in tests and development.
"""

import json
import os

class MockConfig:
    def __init__(self, useMocksDir=None, writeMocksDir=None, useMockSuffix="mock", writeMockSuffix="mock"):
        """
        Initialize mock configuration
        
        Args:
            useMocksDir (str, optional): Directory path where mock responses are read from. 
                                         If set, mocks are loaded and used. Defaults to None.
            writeMocksDir (str, optional): Directory path where mock responses are written to. 
                                           If set, API responses are written to mock files. Defaults to None.
            useMockSuffix (str): Suffix to append to mock filenames (before extension) when reading. Defaults to "mock".
            writeMockSuffix (str): Suffix to append to mock filenames (before extension) when writing. Defaults to "mock".
        """
        self.useMocksDir = useMocksDir
        self.writeMocksDir = writeMocksDir
        self.useMockSuffix = useMockSuffix
        self.writeMockSuffix = writeMockSuffix
    
    def useMocks(self):
        return self.useMocksDir is not None

    def writeMocks(self):
        return self.writeMocksDir is not None
    
    def write_json_mock(self, mock_file, content):
        """
        Write JSON content to a mock file with proper indentation
        
        Args:
            mock_file (str): Base filename to write to (relative to writeMocksDir)
            content (dict): JSON content to write
            
        Returns:
            str: Path to the created mock file, or None if writeMocksDir is not set
        """
        if self.writeMocksDir is None:
            return None
        os.makedirs(self.writeMocksDir, exist_ok=True)
        mock_path = os.path.join(self.writeMocksDir, mock_file)
        
        with open(mock_path, 'w') as f:
            json.dump(content, f, indent=2)
            
        return mock_path
    
    def read_json_mock(self, mock_file):
        """
        Read content from a mock file and return it as a string
        
        Args:
            mock_file (str): Base filename to read from (relative to useMocksDir). Suffix will be applied.
                
        Returns:
            str: File content as a string
            
        Raises:
            FileNotFoundError: If the file is not found
        """
            
        if self.useMocksDir is not None:
            mock_path = os.path.join(self.useMocksDir, mock_file)
            with open(mock_path, 'r') as f:
                return f.read()
        return None
    
    def __str__(self):
        """String representation of the mock configuration"""
        return f"MockConfig[useMocksDir={self.useMocksDir}, writeMocksDir={self.writeMocksDir}, useMockSuffix={self.useMockSuffix}, writeMockSuffix={self.writeMockSuffix}]" 