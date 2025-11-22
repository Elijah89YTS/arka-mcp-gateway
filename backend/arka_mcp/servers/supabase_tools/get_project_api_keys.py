from typing import Any


async def get_project_api_keys(ref: str) -> Any:
    """
    Retrieves all API keys for an existing Supabase project.

    Args:
        ref: The unique reference ID of the Supabase project for which to retrieve API keys.

    Returns:
        Parsed JSON array of API key records from the Supabase management API.

    Example:
        result = await get_project_api_keys("projectref_0123456789abcdef")
        # result might be:
        # {
        #   "data": [
        #     {"id": "anon", "name": "anon", "prefix": "sb_anon_", "hash": "...", "type": "legacy", ...},
        #     {"id": "key_123", "name": "Client Key", "prefix": "sb_pub_", "hash": "...", "type": "publishable", ...}
        #   ],
        #   "error": null,
        #   "successful": true
        # }
    """
    from .client import SupabaseAPIClient

    client = SupabaseAPIClient()
    # Call Supabase management API to list all API keys for the project
    return await client.get(f"/projects/{ref}/api-keys")
