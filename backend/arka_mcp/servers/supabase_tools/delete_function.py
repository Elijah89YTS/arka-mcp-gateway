from typing import Any

async def delete_function(ref: str, function_slug: str) -> Any:
    """
    Permanently deletes a specific Edge Function from a Supabase project.

    Sends a DELETE request to the Supabase Management API
    `/v1/projects/{ref}/functions/{function_slug}` to remove the function.

    Args:
        ref: The unique reference ID of the Supabase project.
        function_slug: The slug identifier of the function to delete.

    Returns:
        Parsed JSON response confirming deletion.

    Example:
        result = await delete_function(ref="projectref_abc123", function_slug="old-fn")
        # result: {"data": {}, "error": null, "successful": true}
    """
    from .client import SupabaseAPIClient

    client = SupabaseAPIClient()
    return await client.delete(f"/projects/{ref}/functions/{function_slug}")
