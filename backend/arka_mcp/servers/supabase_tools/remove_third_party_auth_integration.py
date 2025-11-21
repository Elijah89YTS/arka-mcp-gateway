from typing import Any


async def remove_third_party_auth_integration(ref: str, tpa_id: str) -> Any:
    """
    Removes a third-party authentication provider from a Supabase project's configuration.

    Args:
        ref: The unique reference ID of the Supabase project.
        tpa_id: The unique identifier of the third-party auth provider to remove.

    Returns:
        Parsed JSON response confirming removal.

    Example:
        result = await remove_third_party_auth_integration(
            ref="projectref_012345",
            tpa_id="github-oauth"
        )
        # result might be:
        # {"data": {...}, "error": null, "successful": true}
    """
    from .client import SupabaseAPIClient

    client = SupabaseAPIClient()
    return await client.delete(f"/projects/{ref}/config/auth/third-party-auth/{tpa_id}")
