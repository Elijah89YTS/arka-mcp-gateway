"""
GitHub API Client Abstraction.

Provides a thin wrapper over httpx for GitHub API calls with automatic
OAuth token retrieval from worker context.

Security and performance features:
- Reuses AsyncClient instance to avoid resource leaks
- Connection pooling with configurable limits
- Proper error handling for timeouts and network errors
- Sanitized error messages
"""

import httpx
import logging
from typing import Dict, Any, Optional
from fastapi import HTTPException

logger = logging.getLogger(__name__)


class GitHubAPIClient:
    """
    GitHub API client with automatic OAuth token management.

    Handles HTTP communication with GitHub API, including:
    - OAuth token retrieval from worker context
    - Request formatting
    - Error handling
    - Response parsing
    - Connection pooling and reuse

    Usage:
        client = GitHubAPIClient()
        result = await client.get("/user")

    Note: Client instance is created per request but reuses internal connection pool.
    """

    BASE_URL = "https://api.github.com"
    DEFAULT_TIMEOUT = 30.0
    MAX_CONNECTIONS = 20

    # Shared connection pool across instances
    _shared_client: Optional[httpx.AsyncClient] = None

    def __init__(self, timeout: float = DEFAULT_TIMEOUT):
        """
        Initialize GitHub API client.

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
            logger.debug("Created shared GitHub API client with connection pooling")
        return cls._shared_client

    @classmethod
    async def close_shared_client(cls):
        """Close shared client connection pool. Call during shutdown."""
        if cls._shared_client is not None:
            await cls._shared_client.aclose()
            cls._shared_client = None
            logger.debug("Closed shared GitHub API client")

    def _get_access_token(self) -> str:
        """
        Get OAuth access token from worker context.

        Returns:
            Access token string

        Raises:
            RuntimeError: If no token context available
            ValueError: If github-mcp not authorized
        """
        from arka_mcp.servers.worker_context import get_oauth_token

        token_data = get_oauth_token("github-mcp")
        return token_data["access_token"]

    def _handle_request_error(self, error: Exception, operation: str) -> None:
        """
        Handle HTTP request errors with appropriate logging and exceptions.

        Args:
            error: The caught exception
            operation: Description of the operation (e.g., "GET /user")

        Raises:
            HTTPException: With appropriate status code and sanitized message
        """
        if isinstance(error, httpx.TimeoutException):
            logger.error(f"GitHub API timeout during {operation}: {error}")
            raise HTTPException(
                status_code=504,
                detail="GitHub API request timed out. Please try again."
            )
        elif isinstance(error, httpx.HTTPStatusError):
            status_code = error.response.status_code
            logger.error(
                f"GitHub API HTTP error during {operation}: "
                f"status={status_code}, details={error}"
            )
            # Pass through GitHub API errors with sanitized messages
            if status_code == 401:
                detail = "GitHub authentication failed. Please reauthorize."
            elif status_code == 403:
                detail = "GitHub API rate limit or permission denied."
            elif status_code == 404:
                detail = "GitHub resource not found."
            else:
                detail = f"GitHub API error (status {status_code})"
            raise HTTPException(status_code=status_code, detail=detail)
        elif isinstance(error, httpx.RequestError):
            logger.error(f"GitHub API network error during {operation}: {error}")
            raise HTTPException(
                status_code=503,
                detail="Failed to connect to GitHub API. Please check your connection."
            )
        else:
            logger.error(f"Unexpected error during {operation}: {error}")
            raise HTTPException(
                status_code=500,
                detail="An unexpected error occurred while accessing GitHub API."
            )

    async def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """
        Make GET request to GitHub API.

        Args:
            endpoint: API endpoint (e.g., "/user")
            params: Optional query parameters

        Returns:
            Parsed JSON response

        Raises:
            HTTPException: If request fails
        """
        access_token = self._get_access_token()
        url = f"{self.BASE_URL}{endpoint}"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

        client = self._get_client()
        try:
            response = await client.get(
                url,
                headers=headers,
                params=params,
                timeout=self.timeout,
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self._handle_request_error(e, f"GET {endpoint}")

    async def post(
        self,
        endpoint: str,
        json_data: Dict[str, Any],
        params: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """
        Make POST request to GitHub API.

        Args:
            endpoint: API endpoint (e.g., "/repos/{owner}/{repo}/issues")
            json_data: Request body as dictionary
            params: Optional query parameters

        Returns:
            Parsed JSON response

        Raises:
            HTTPException: If request fails
        """
        access_token = self._get_access_token()
        url = f"{self.BASE_URL}{endpoint}"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Content-Type": "application/json",
        }

        client = self._get_client()
        try:
            response = await client.post(
                url,
                headers=headers,
                json=json_data,
                params=params,
                timeout=self.timeout,
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self._handle_request_error(e, f"POST {endpoint}")

    async def patch(
        self,
        endpoint: str,
        json_data: Dict[str, Any],
        params: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """
        Make PATCH request to GitHub API.

        Args:
            endpoint: API endpoint
            json_data: Request body as dictionary
            params: Optional query parameters

        Returns:
            Parsed JSON response

        Raises:
            HTTPException: If request fails
        """
        access_token = self._get_access_token()
        url = f"{self.BASE_URL}{endpoint}"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Content-Type": "application/json",
        }

        client = self._get_client()
        try:
            response = await client.patch(
                url,
                headers=headers,
                json=json_data,
                params=params,
                timeout=self.timeout,
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self._handle_request_error(e, f"PATCH {endpoint}")

    async def put(
        self,
        endpoint: str,
        json_data: Dict[str, Any],
        params: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """
        Make PUT request to GitHub API.

        Args:
            endpoint: API endpoint (e.g., "/repos/{owner}/{repo}/pulls/{number}/merge").
            json_data: Request body as dictionary.
            params: Optional query parameters.

        Returns:
            Parsed JSON response.

        Raises:
            HTTPException: If request fails.
        """
        access_token = self._get_access_token()
        url = f"{self.BASE_URL}{endpoint}"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Content-Type": "application/json",
        }

        client = self._get_client()
        try:
            response = await client.put(
                url,
                headers=headers,
                json=json_data,
                params=params,
                timeout=self.timeout,
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self._handle_request_error(e, f"PUT {endpoint}")

    async def delete(
        self, endpoint: str, params: Optional[Dict[str, Any]] = None
    ) -> Any:
        """
        Make DELETE request to GitHub API.

        Args:
            endpoint: API endpoint (e.g., "/repos/{owner}/{repo}")
            params: Optional query parameters

        Returns:
            Parsed JSON response or empty dict

        Raises:
            HTTPException: If request fails
        """
        access_token = self._get_access_token()
        url = f"{self.BASE_URL}{endpoint}"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

        client = self._get_client()
        try:
            response = await client.delete(
                url,
                headers=headers,
                params=params,
                timeout=self.timeout,
            )
            response.raise_for_status()
            # Some DELETE endpoints return no content
            if response.text:
                return response.json()
            return {}
        except Exception as e:
            self._handle_request_error(e, f"DELETE {endpoint}")
