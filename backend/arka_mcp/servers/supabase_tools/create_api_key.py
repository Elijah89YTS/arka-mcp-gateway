from typing import Any, Dict, Optional


async def create_api_key(
    ref: str, name: str, type: str, description: Optional[str] = None
) -> Any:
    """
    Creates a 'publishable' or 'secret' API key for an existing Supabase project.

    Args:
        ref: The unique reference ID of the Supabase project.
        name: Human-readable name for the API key.
        type: The type of API key: 'publishable' or 'secret'.
        description: Optional description for the API key.

    Returns:
        Parsed JSON response containing the new API key data.

    Example:
        result = await create_api_key(
            ref="projectref_012345",
            name="Client Key",
            type="publishable",
            description="Key for public client usage"
        )
        # result might be:
        # {"data": {"id": "key_123", "prefix": "pubk_", ...}, "error": null, "successful": true}
    """
    from .client import SupabaseAPIClient

    client = SupabaseAPIClient()
    payload: Dict[str, Any] = {"name": name, "type": type}
    if description is not None:
        payload["description"] = description
    return await client.post(f"/projects/{ref}/api-keys", json_data=payload)
