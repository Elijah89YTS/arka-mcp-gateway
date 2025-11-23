"""
Fetches the authenticated user's task lists from Google Tasks; results may be paginated.

Google Tasks API Reference:
https://developers.google.com/tasks/reference/rest/v1/tasklists/list
"""
from typing import Optional, Dict, Any
from .client import TasksAPIClient


async def list_task_lists(
    max_results: int = 20,
    page_token: Optional[str] = None
) -> dict:
    """
    Retrieves the authenticated user's task lists.

    Args:
        max_results: Maximum number of task lists to return per page.
        page_token: Token for the page of results to return; omit for first page.

    Returns:
        Dict containing 'items' (list of task lists) and optional 'nextPageToken'.

    Example:
        result = await list_task_lists(max_results=10)
        items = result.get('items', [])
        next_token = result.get('nextPageToken')
    """
    client = TasksAPIClient()
    params: Dict[str, Any] = {'maxResults': max_results}
    if page_token:
        params['pageToken'] = page_token

    endpoint = "/users/@me/lists"
    # Raw API response includes 'items' and 'nextPageToken'
    return await client.get(endpoint, params=params)
