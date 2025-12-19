"""GCS (Google Cloud Storage) service for file operations."""
import re
from typing import List, Dict
from google.cloud import storage
import pandas as pd
import io


class GCSService:
    """Service for GCS file operations."""
    
    def __init__(self):
        """Initialize GCS service."""
        self._client = None

    @property
    def client(self):
        """Lazy load GCS client."""
        if not self._client:
            self._client = storage.Client()
        return self._client
    
    async def resolve_pattern(self, bucket_name: str, pattern: str) -> List[str]:
        """
        Resolve wildcard patterns in GCS file paths.
        
        Args:
            bucket_name: GCS bucket name
            pattern: File path pattern (supports * wildcard)
            
        Returns:
            List of matching file paths
            
        Raises:
            ValueError: If no files match the pattern
        """
        # If no wildcard, return as-is
        if '*' not in pattern:
            return [pattern]
        
        try:
            bucket = self.client.bucket(bucket_name)
            
            # Get prefix before wildcard
            prefix = pattern.split('*')[0]
            
            # List files with prefix
            blobs = bucket.list_blobs(prefix=prefix)
            
            # Convert pattern to regex
            regex_pattern = pattern.replace('*', '.*')
            regex = re.compile(f'^{regex_pattern}$')
            
            # Filter matching files
            matching_files = [
                blob.name for blob in blobs
                if regex.match(blob.name)
            ]
            
            if not matching_files:
                raise ValueError(
                    f"No files found matching pattern: gs://{bucket_name}/{pattern}"
                )
            
            return matching_files
            
        except Exception as e:
            raise ValueError(
                f"Failed to resolve pattern gs://{bucket_name}/{pattern}: {str(e)}"
            )
    
    async def count_csv_rows(self, bucket_name: str, file_path: str) -> int:
        """
        Count rows in a CSV file.
        
        Args:
            bucket_name: GCS bucket name
            file_path: Path to CSV file
            
        Returns:
            Number of rows (excluding header)
        """
        try:
            bucket = self.client.bucket(bucket_name)
            blob = bucket.blob(file_path)
            
            if not blob.exists():
                raise FileNotFoundError(
                    f"File not found: gs://{bucket_name}/{file_path}"
                )
            
            # Download and count rows using pandas
            content = blob.download_as_bytes()
            df = pd.read_csv(io.BytesIO(content))
            
            return len(df)
            
        except Exception as e:
            raise ValueError(
                f"Failed to count rows in gs://{bucket_name}/{file_path}: {str(e)}"
            )
    
    async def sample_csv_data(
        self, 
        bucket_name: str, 
        file_path: str, 
        limit: int = 100
    ) -> List[Dict]:
        """
        Sample data from a CSV file.
        
        Args:
            bucket_name: GCS bucket name
            file_path: Path to CSV file
            limit: Maximum number of rows to return
            
        Returns:
            List of dictionaries representing rows
        """
        try:
            bucket = self.client.bucket(bucket_name)
            blob = bucket.blob(file_path)
            
            if not blob.exists():
                raise FileNotFoundError(
                    f"File not found: gs://{bucket_name}/{file_path}"
                )
            
            # Download and sample using pandas
            content = blob.download_as_bytes()
            df = pd.read_csv(io.BytesIO(content), nrows=limit)
            
            # Convert to list of dicts
            return df.to_dict('records')
            
        except Exception as e:
            raise ValueError(
                f"Failed to sample data from gs://{bucket_name}/{file_path}: {str(e)}"
            )
    
    async def get_csv_headers(self, bucket_name: str, file_path: str) -> List[str]:
        """
        Get column headers from a CSV file.
        
        Args:
            bucket_name: GCS bucket name
            file_path: Path to CSV file
            
        Returns:
            List of column names
        """
        try:
            bucket = self.client.bucket(bucket_name)
            blob = bucket.blob(file_path)
            
            if not blob.exists():
                raise FileNotFoundError(
                    f"File not found: gs://{bucket_name}/{file_path}"
                )
            
            # Download and get headers using pandas
            content = blob.download_as_bytes()
            df = pd.read_csv(io.BytesIO(content), nrows=0)
            
            return df.columns.tolist()
            
        except Exception as e:
            raise ValueError(
                f"Failed to get headers from gs://{bucket_name}/{file_path}: {str(e)}"
            )


# Singleton instance
gcs_service = GCSService()
