"""
Supabase client configuration and utilities.
Infrastructure layer - External service integration.
"""
import os
from supabase import create_client, Client
from typing import Optional


class SupabaseService:
    """
    Supabase client service following Single Responsibility Principle.
    Handles Supabase client initialization and common operations.
    """
    
    _instance: Optional['SupabaseService'] = None
    _client: Optional[Client] = None
    
    def __new__(cls) -> 'SupabaseService':
        """Singleton pattern for Supabase client."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize Supabase client if not already initialized."""
        if self._client is None:
            self._initialize_client()
    
    def _initialize_client(self) -> None:
        """Initialize the Supabase client with environment variables."""
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_ANON_KEY')
        
        if not supabase_url or not supabase_key:
            print("⚠️  Supabase URL or ANON_KEY not configured. Supabase client not available.")
            return
        
        try:
            self._client = create_client(supabase_url, supabase_key)
            print("✅ Supabase client initialized successfully")
        except Exception as e:
            print(f"❌ Error initializing Supabase client: {e}")
            self._client = None
    
    @property
    def client(self) -> Optional[Client]:
        """Get the Supabase client instance."""
        return self._client
    
    def is_available(self) -> bool:
        """Check if Supabase client is available."""
        return self._client is not None
    
    def test_connection(self) -> bool:
        """Test the Supabase connection."""
        if not self.is_available():
            return False
        
        try:
            # Simple test query - this will work even with an empty database
            self._client.table('pg_stat_database').select('datname').limit(1).execute()
            return True
        except Exception as e:
            print(f"❌ Supabase connection test failed: {e}")
            return False


# Global instance
supabase_service = SupabaseService()


def get_supabase_client() -> Optional[Client]:
    """
    Get the global Supabase client instance.
    
    Returns:
        Optional[Client]: Supabase client or None if not configured
    """
    return supabase_service.client


def test_supabase_connection() -> bool:
    """
    Test the Supabase connection.
    
    Returns:
        bool: True if connection is successful, False otherwise
    """
    return supabase_service.test_connection()