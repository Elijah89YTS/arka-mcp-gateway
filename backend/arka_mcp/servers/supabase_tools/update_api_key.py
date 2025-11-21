from typing import Any, Dict, Optional


async def update_api_key(
    ref: str,
    id: str,
    description: Optional[str] = None,
    secret_jwt_template: Optional[Dict[str, Any]] = None,
) -> Any:
    """
    Updates an existing Supabase project API key's description and/or secret JWT template.

    Args:
        ref: The unique reference ID of the Supabase project.
        id: The unique identifier of the API key to update.
        description: Optional new description for the API key.
        secret_jwt_template: Optional JWT template object for secret keys.

    Returns:
        Parsed JSON response containing the updated API key data.

    Example:
        result = await update_api_key(
            ref="projectref_012345",
            id="key_123",
            description="Updated description",
            secret_jwt_template={"role": "admin"}
        )
        # result might be:
        # {"data": {"id": "key_123", "description": "Updated description", ...}, "error": null, "successful": true}
    """
    from .client import SupabaseAPIClient

    client = SupabaseAPIClient()
    payload: Dict[str, Any] = {}
    if description is not None:
        payload["description"] = description
    if secret_jwt_template is not None:
        payload["secret_jwt_template"] = secret_jwt_template
    return await client.patch(f"/projects/{ref}/api-keys/{id}", json_data=payload)
