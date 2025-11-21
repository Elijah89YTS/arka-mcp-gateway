from typing import Any


async def list_secrets(ref: str) -> Any:
    """
    Retrieves all secrets for a Supabase project using its reference ID; secret values in the response may be masked.

    Args:
        ref: The unique reference ID of the Supabase project whose secrets are to be retrieved.

    Returns:
        Parsed JSON response from the Supabase management API.

    Example:
        result = await list_secrets("projectref_0123456789abcdef")
        # result might be:
        # {
        #   "data": [
        #     {"name": "API_KEY", "value": "****", "updated_at": "2025-01-01T00:00:00Z"}
        #   ],
        #   "error": null,
        #   "successful": true
        # }
    """
    from .client import SupabaseAPIClient

    client = SupabaseAPIClient()
    # Call Supabase management API to list secrets for the project
    return await client.get(f"/projects/{ref}/secrets")
