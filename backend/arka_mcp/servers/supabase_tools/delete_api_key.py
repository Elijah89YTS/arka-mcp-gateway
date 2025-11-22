from typing import Any


async def delete_api_key(ref: str, id: str) -> Any:
    """
    Permanently deletes a specific API key from a Supabase project, revoking its access.

    Args:
        ref: The unique reference ID of the Supabase project.
        id: The unique identifier of the API key to delete.

    Returns:
        Parsed JSON response confirming deletion.

    Example:
        result = await delete_api_key(
            ref="projectref_012345",
            id="key_123"
        )
        # result might be:
        # {"data": {...}, "error": null, "successful": true}
    """
    from .client import SupabaseAPIClient

    client = SupabaseAPIClient()
    return await client.delete(f"/projects/{ref}/api-keys/{id}")
