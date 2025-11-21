from typing import Any


async def list_members_of_an_organization(slug: str) -> Any:
    """
    Retrieves all members of a Supabase organization, identified by its unique slug, including their user ID, username, email, role, and MFA status.

    Args:
        slug: The unique identifier (slug) of the organization for which to list members.

    Returns:
        Parsed JSON response from the Supabase management API.

    Example:
        result = await list_members_of_an_organization("my-supabase-org")
        # result might be:
        # {
        #   "data": [
        #     {"user_id": "user123", "user_name": "jdoe", "email": "jdoe@example.com", "role_name": "owner", "mfa_enabled": true}
        #   ],
        #   "error": null,
        #   "successful": true
        # }
    """
    from .client import SupabaseAPIClient

    client = SupabaseAPIClient()
    # Call Supabase management API to list organization members
    return await client.get(f"/organizations/{slug}/members")
