from typing import Any


async def list_third_party_auth_integrations(ref: str) -> Any:
    """
    Lists all configured third-party authentication provider integrations for a Supabase project.

    Args:
        ref: The unique reference ID of the Supabase project.

    Returns:
        Parsed JSON response containing an array of integrations.

    Example:
        result = await list_third_party_auth_integrations("projectref_012345")
        # result might be:
        # {"data": [{"id": "google-oauth", "type": "google", ...}], "error": null, "successful": true}
    """
    from .client import SupabaseAPIClient

    client = SupabaseAPIClient()
    return await client.get(f"/projects/{ref}/config/auth/third-party-auth")
