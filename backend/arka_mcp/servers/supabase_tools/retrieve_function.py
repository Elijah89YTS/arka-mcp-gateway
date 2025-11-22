from typing import Any

async def retrieve_function(ref: str, function_slug: str) -> Any:
    """
    Retrieves detailed metadata for a specific Edge Function.

    Fetches function configuration, lifecycle status, and version via
    the Supabase Management API `/v1/projects/{ref}/functions/{function_slug}`.

    Args:
        ref: The unique reference ID of the Supabase project.
        function_slug: The slug identifier of the function to retrieve.

    Returns:
        Parsed JSON response with the function's metadata.

    Example:
        result = await retrieve_function(ref="projectref_abc123", function_slug="my-fn")
        # result: {"data": {"id": "...", "slug": "my-fn", ...}, "error": null, "successful": true}
    """
    from .client import SupabaseAPIClient

    client = SupabaseAPIClient()
    return await client.get(f"/projects/{ref}/functions/{function_slug}")
