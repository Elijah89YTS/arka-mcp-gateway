from typing import Any


async def list_projects() -> Any:
    """
    List all Supabase projects for the authenticated user.

    Retrieves project data via the Supabase management API `/v1/projects`.

    Args:
        None

    Returns:
        Parsed JSON response from the Supabase management API.

    Example:
        result = await list_projects()
        # result might be:
        # {
        #   "data": [
        #       {"id": "proj1", "name": "My Project", "region": "us-east-1", ...}
        #   ],
        #   "error": null,
        #   "successful": true
        # }
    """
    from .client import SupabaseAPIClient

    client = SupabaseAPIClient()
    # Call Supabase management API to list projects
    return await client.get("/projects")
