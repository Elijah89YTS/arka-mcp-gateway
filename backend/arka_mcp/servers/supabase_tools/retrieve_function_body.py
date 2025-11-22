from typing import Any

async def retrieve_function_body(ref: str, function_slug: str) -> Any:
    """
    Retrieves the source code body of a specific Edge Function.

    Fetches raw function code via the Supabase Management API
    `/v1/projects/{ref}/functions/{function_slug}/body`.

    Args:
        ref: The unique reference ID of the Supabase project.
        function_slug: The slug identifier of the function.

    Returns:
        Parsed JSON response or raw text containing the function's source code.

    Example:
        result = await retrieve_function_body(
            ref="projectref_abc123", function_slug="my-fn"
        )
        # result: {"data": {...}, "error": null, "successful": true}
    """
    from .client import SupabaseAPIClient

    client = SupabaseAPIClient()
    return await client.get(
        f"/projects/{ref}/functions/{function_slug}/body"
    )
