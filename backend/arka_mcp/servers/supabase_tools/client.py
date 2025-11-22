"""
Supabase API Client Abstraction.

Provides a thin wrapper over httpx for Supabase management API calls with automatic
OAuth token retrieval from worker context.
"""

import httpx
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class SupabaseAPIClient:
    """
    Supabase API client with automatic OAuth token management.

    Handles HTTP communication with Supabase management API, including:
    - OAuth token retrieval from worker context
    - Request formatting
    - Error handling
    """

    BASE_URL = "https://api.supabase.com/v1"
    DEFAULT_TIMEOUT = 30.0

    def __init__(self, timeout: float = DEFAULT_TIMEOUT):
        """
        Initialize Supabase API client.

        Args:
            timeout: Request timeout in seconds (default: 30.0)
        """
        self.timeout = timeout

    def _get_access_token(self) -> str:
        """
        Get OAuth access token from worker context.

        Returns:
            Access token string

        Raises:
            RuntimeError: If no token context available
            ValueError: If supabase-mcp not authorized
        """
        from arka_mcp.servers.worker_context import get_oauth_token

        token_data = get_oauth_token("supabase-mcp")
        return token_data["access_token"]

    async def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """
        Make GET request to Supabase management API.

        Args:
            endpoint: API endpoint (e.g., "/projects")
            params: Optional query parameters

        Returns:
            API response as parsed JSON

        Raises:
            httpx.HTTPStatusError: If request fails
        """
        access_token = self._get_access_token()
        url = f"{self.BASE_URL}{endpoint}"

        async with httpx.AsyncClient() as http_client:
            response = await http_client.get(
                url,
                headers={"Authorization": f"Bearer {access_token}"},
                params=params,
                timeout=self.timeout,
            )
            response.raise_for_status()
            return response.json()

    async def post(
        self,
        endpoint: str,
        json_data: Dict[str, Any],
        params: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """
        Make POST request to Supabase management API.

        Args:
            endpoint: API endpoint (e.g., "/projects/{ref}/keys")
            json_data: Request body as dictionary
            params: Optional query parameters

        Returns:
            Parsed JSON response

        Raises:
            httpx.HTTPStatusError: If request fails
        """
        access_token = self._get_access_token()
        url = f"{self.BASE_URL}{endpoint}"
        async with httpx.AsyncClient() as http_client:
            response = await http_client.post(
                url,
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/json",
                },
                json=json_data,
                params=params,
                timeout=self.timeout,
            )
            response.raise_for_status()
            return response.json()

    async def delete(
        self, endpoint: str, params: Optional[Dict[str, Any]] = None
    ) -> Any:
        """
        Make DELETE request to Supabase management API.

        Args:
            endpoint: API endpoint (e.g., "/projects/{ref}/keys/{id}")
            params: Optional query parameters

        Returns:
            Parsed JSON response

        Raises:
            httpx.HTTPStatusError: If request fails
        """
        access_token = self._get_access_token()
        url = f"{self.BASE_URL}{endpoint}"
        async with httpx.AsyncClient() as http_client:
            response = await http_client.delete(
                url,
                headers={"Authorization": f"Bearer {access_token}"},
                params=params,
                timeout=self.timeout,
            )
            response.raise_for_status()
            return response.json()

    async def patch(
        self,
        endpoint: str,
        json_data: Dict[str, Any],
        params: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """
        Make PATCH request to Supabase management API.

        Args:
            endpoint: API endpoint
            json_data: Request body as dictionary
            params: Optional query parameters

        Returns:
            Parsed JSON response

        Raises:
            httpx.HTTPStatusError: If request fails
        """
        access_token = self._get_access_token()
        url = f"{self.BASE_URL}{endpoint}"
        async with httpx.AsyncClient() as http_client:
            response = await http_client.patch(
                url,
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/json",
                },
                json=json_data,
                params=params,
                timeout=self.timeout,
            )
            response.raise_for_status()
            return response.json()
