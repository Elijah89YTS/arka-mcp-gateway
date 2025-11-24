"""
Google Tasks API Client Abstraction.

Provides a thin wrapper over httpx for Google Tasks API calls with automatic
OAuth token retrieval from worker context.

Security and performance features:
- Reuses AsyncClient instance to avoid resource leaks
- Connection pooling with configurable limits
- Proper error handling for timeouts and network errors
- Sanitized error messages
- Clean API for GET/POST/PATCH/DELETE operations

Usage:
    from gtasks_tools.client import TasksAPIClient

    client = TasksAPIClient()
    lists = await client.get("/users/@me/lists")
"""

import httpx
import logging
from typing import Dict, Any, Optional
from fastapi import HTTPException

logger = logging.getLogger(__name__)


class TasksAPIClient:
    """
    Google Tasks API client with automatic OAuth token management.

    Handles all HTTP communication with Google Tasks API, including:
    - OAuth token retrieval from worker_context
    - Request formatting
    - Error handling
    - Response parsing
    - Connection pooling and reuse

    Usage:
        client = TasksAPIClient()
        result = await client.get("/users/@me/lists")

    Note: Client instance is created per request but reuses internal connection pool.
    """

    BASE_URL = "https://tasks.googleapis.com/tasks/v1"
    DEFAULT_TIMEOUT = 30.0
    MAX_CONNECTIONS = 20

    # Shared connection pool across instances
    _shared_client: Optional[httpx.AsyncClient] = None

    def __init__(self, timeout: float = DEFAULT_TIMEOUT):
        """
        Initialize Google Tasks API client.

        Args:
            timeout: Request timeout in seconds (default: 30.0)
        """
        self.timeout = timeout

    @classmethod
    def _get_client(cls) -> httpx.AsyncClient:
        """
        Get or create shared AsyncClient instance.

        Returns:
            Shared httpx.AsyncClient with connection pooling

        Note: Uses class-level singleton to avoid creating new clients per request
        """
        if cls._shared_client is None:
            cls._shared_client = httpx.AsyncClient(
                limits=httpx.Limits(
                    max_keepalive_connections=cls.MAX_CONNECTIONS,
                    max_connections=cls.MAX_CONNECTIONS * 2,
                ),
                timeout=cls.DEFAULT_TIMEOUT,
            )
            logger.debug("Created shared Google Tasks API client with connection pooling")
        return cls._shared_client

    @classmethod
    async def close_shared_client(cls):
        """Close shared client connection pool. Call during shutdown."""
        if cls._shared_client is not None:
            await cls._shared_client.aclose()
            cls._shared_client = None
            logger.debug("Closed shared Google Tasks API client")

    def _get_access_token(self) -> str:
        """
        Get OAuth access token from worker context.

        Returns:
            Access token string

        Raises:
            RuntimeError: If no token context available
            ValueError: If gtasks-mcp not authorized
        """
        from arka_mcp.servers.worker_context import get_oauth_token

        token_data = get_oauth_token("gtasks-mcp")
        return token_data["access_token"]

    def _handle_request_error(self, error: Exception, operation: str) -> None:
        """
        Handle HTTP request errors with appropriate logging and exceptions.

        Args:
            error: The caught exception
            operation: Description of the operation (e.g., "GET /users/@me/lists")

        Raises:
            HTTPException: With appropriate status code and sanitized message
        """
        if isinstance(error, httpx.TimeoutException):
            logger.error(f"Google Tasks API timeout during {operation}: {error}")
            raise HTTPException(
                status_code=504,
                detail="Google Tasks API request timed out. Please try again."
            )
        elif isinstance(error, httpx.HTTPStatusError):
            status_code = error.response.status_code
            logger.error(
                f"Google Tasks API HTTP error during {operation}: "
                f"status={status_code}, details={error}"
            )
            # Pass through Google API errors with sanitized messages
            if status_code == 401:
                detail = "Google Tasks authentication failed. Please reauthorize."
            elif status_code == 403:
                detail = "Google Tasks API rate limit or permission denied."
            elif status_code == 404:
                detail = "Google Tasks resource not found."
            else:
                detail = f"Google Tasks API error (status {status_code})"
            raise HTTPException(status_code=status_code, detail=detail)
        elif isinstance(error, httpx.RequestError):
            logger.error(f"Google Tasks API network error during {operation}: {error}")
            raise HTTPException(
                status_code=503,
                detail="Failed to connect to Google Tasks API. Please check your connection."
            )
        else:
            logger.error(f"Unexpected error during {operation}: {error}")
            raise HTTPException(
                status_code=500,
                detail="An unexpected error occurred while accessing Google Tasks API."
            )

    async def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make GET request to Google Tasks API.

        Args:
            endpoint: API endpoint (e.g., "/users/@me/lists")
            params: Optional query parameters

        Returns:
            API response as dictionary

        Raises:
            HTTPException: If request fails

        Example:
            lists = await client.get("/users/@me/lists")
            tasks = await client.get(f"/lists/{list_id}/tasks", {"maxResults": 10})
        """
        access_token = self._get_access_token()
        url = f"{self.BASE_URL}{endpoint}"

        client = self._get_client()
        try:
            response = await client.get(
                url,
                headers={"Authorization": f"Bearer {access_token}"},
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self._handle_request_error(e, f"GET {endpoint}")

    async def post(
        self,
        endpoint: str,
        json_data: Dict[str, Any],
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make POST request to Google Tasks API.

        Args:
            endpoint: API endpoint
            json_data: Request body as dictionary
            params: Optional query parameters

        Returns:
            API response as dictionary

        Raises:
            HTTPException: If request fails

        Example:
            new_list = await client.post(
                "/users/@me/lists",
                {"title": "My Tasks"}
            )
        """
        access_token = self._get_access_token()
        url = f"{self.BASE_URL}{endpoint}"

        client = self._get_client()
        try:
            response = await client.post(
                url,
                headers={"Authorization": f"Bearer {access_token}"},
                json=json_data,
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self._handle_request_error(e, f"POST {endpoint}")

    async def patch(
        self,
        endpoint: str,
        json_data: Dict[str, Any],
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make PATCH request to Google Tasks API.

        Args:
            endpoint: API endpoint
            json_data: Request body as dictionary
            params: Optional query parameters

        Returns:
            API response as dictionary

        Raises:
            HTTPException: If request fails

        Example:
            updated = await client.patch(
                f"/lists/{list_id}/tasks/{task_id}",
                {"status": "completed"}
            )
        """
        access_token = self._get_access_token()
        url = f"{self.BASE_URL}{endpoint}"

        client = self._get_client()
        try:
            response = await client.patch(
                url,
                headers={"Authorization": f"Bearer {access_token}"},
                json=json_data,
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self._handle_request_error(e, f"PATCH {endpoint}")

    async def delete(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Make DELETE request to Google Tasks API.

        Args:
            endpoint: API endpoint
            params: Optional query parameters

        Returns:
            True if deletion successful, False otherwise

        Raises:
            HTTPException: If request fails

        Example:
            success = await client.delete(f"/lists/{list_id}")
        """
        access_token = self._get_access_token()
        url = f"{self.BASE_URL}{endpoint}"

        client = self._get_client()
        try:
            response = await client.delete(
                url,
                headers={"Authorization": f"Bearer {access_token}"},
                params=params,
                timeout=self.timeout
            )
            if response.status_code in (200, 204):
                return True
            response.raise_for_status()
            return False
        except Exception as e:
            self._handle_request_error(e, f"DELETE {endpoint}")
