from typing import Any


async def list_organizations() -> Any:
    """
    Lists all organizations (ID and name only) associated with the Supabase account, excluding project details within these organizations.

    Args:
        None

    Returns:
        Parsed JSON response from the Supabase management API.

    Example:
        result = await list_organizations()
        # result might be:
        # {
        #   "data": [
        #       {"id": "org1", "name": "My Org"},
        #       {"id": "org2", "name": "Another Org"}
        #   ],
        #   "error": null,
        #   "successful": true
        # }
    """
    from .client import SupabaseAPIClient

    client = SupabaseAPIClient()
    # Call Supabase management API to list organizations
    return await client.get("/organizations")
