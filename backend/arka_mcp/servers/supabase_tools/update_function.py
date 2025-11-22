from typing import Any, Optional, Dict

async def update_function(
    ref: str,
    function_slug: str,
    body: Optional[str] = None,
    name: Optional[str] = None,
    slug: Optional[str] = None,
    entrypoint_path: Optional[str] = None,
    import_map: Optional[bool] = None,
    import_map_path: Optional[str] = None,
    verify_jwt: Optional[bool] = None
) -> Any:
    """
    Updates an existing Edge Function's configuration or code.

    Sends updated metadata or source to Supabase Management API
    via PATCH `/v1/projects/{ref}/functions/{function_slug}`.

    Args:
        ref: The unique reference ID of the Supabase project.
        function_slug: The slug of the function to update.
        body: New source code or ESZIP content for the function.
        name: Optional new human-readable name.
        slug: Optional new slug (changes function URL).
        entrypoint_path: Optional updated entrypoint file path.
        import_map: Optional flag to enable/disable import maps.
        import_map_path: Optional path for import map JSON.
        verify_jwt: Optional flag to require JWT verification.

    Returns:
        Parsed JSON response containing updated function metadata.

    Example:
        result = await update_function(
            ref="projectref_abc123",
            function_slug="my-fn",
            name="Renamed Function",
            body="export default () => new Response('Updated');"
        )
    """
    from .client import SupabaseAPIClient

    client = SupabaseAPIClient()
    payload: Dict[str, Any] = {}
    if body is not None:
        payload["body"] = body
    if name is not None:
        payload["name"] = name
    if slug is not None:
        payload["slug"] = slug
    if entrypoint_path is not None:
        payload["entrypoint_path"] = entrypoint_path
    if import_map is not None:
        payload["import_map"] = import_map
    if import_map_path is not None:
        payload["import_map_path"] = import_map_path
    if verify_jwt is not None:
        payload["verify_jwt"] = verify_jwt
    return await client.patch(
        f"/projects/{ref}/functions/{function_slug}", json_data=payload
    )
