from typing import Any


async def get_third_party_integration(ref: str, tpa_id: str) -> Any:
    """
    Retrieves the detailed configuration for a specific third-party authentication provider in a Supabase project.

    Args:
        ref: The unique reference ID of the Supabase project.
        tpa_id: The unique identifier of the third-party auth provider.

    Returns:
        Parsed JSON response containing the provider configuration.

    Example:
        result = await get_third_party_integration(
            ref="projectref_012345",
            tpa_id="google-oauth"
        )
        # result might be:
        # {"data": {"id": "google-oauth", "type": "google", ...}, "error": null, "successful": true}
    """
    from .client import SupabaseAPIClient

    client = SupabaseAPIClient()
    return await client.get(f"/projects/{ref}/config/auth/third-party-auth/{tpa_id}")
