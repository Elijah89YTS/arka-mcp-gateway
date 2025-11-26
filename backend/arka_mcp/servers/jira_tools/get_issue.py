from typing import Any
from .client import JiraAPIClient

async def get_issue(issue_key: str) -> Any:
    """
    Retrieves detailed information about a specific Jira issue.

    Args:
        issue_key: The key of the issue (e.g., "PROJ-123").

    Returns:
        Parsed JSON response from the Jira API.
    """
    client = JiraAPIClient()
    endpoint = f"/issue/{issue_key}"
    return await client.get(endpoint)
