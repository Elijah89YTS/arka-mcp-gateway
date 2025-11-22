from typing import Any

async def list_all_functions(ref: str) -> Any:
    """
    Lists metadata for all Edge Functions in a Supabase project.

    Retrieves function IDs, slugs, names, status, and version via the
    Supabase Management API `/v1/projects/{ref}/functions`.

    Args:
        ref: The unique reference ID of the Supabase project.

    Returns:
        Parsed JSON response containing an array of function metadata.

    Example:
        result = await list_all_functions(ref="projectref_abc123")
        # result: {"data": [{"id": "...", "slug": "fn1", ...}], "error": null, "successful": true}
    """
    from .client import SupabaseAPIClient

    client = SupabaseAPIClient()
    return await client.get(f"/projects/{ref}/functions")
