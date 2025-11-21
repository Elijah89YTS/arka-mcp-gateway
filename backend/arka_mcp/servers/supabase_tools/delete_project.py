from typing import Any


async def delete_project(ref: str) -> Any:
    """
    Permanently deletes a Supabase project by its reference ID, resulting in complete data loss.

    Args:
        ref: Unique reference ID of the Supabase project to delete.

    Returns:
        Parsed JSON response confirming deletion.

    Example:
        result = await delete_project("projectref_abcdefghijkl")
        # result might be:
        # {"data": {"id": 123, "name": "my-app", "ref": "projectref_abcdefghijkl"}, "error": null, "successful": true}
    """
    from .client import SupabaseAPIClient

    client = SupabaseAPIClient()
    # Endpoint: DELETE /v1/projects/{ref}
    return await client.delete(f"/projects/{ref}")
