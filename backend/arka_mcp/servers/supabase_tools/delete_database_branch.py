from typing import Any


async def delete_database_branch(branch_id: str) -> Any:
    """
    Permanently and irreversibly deletes a specific, non-default database branch by its ID.

    Args:
        branch_id: The unique identifier of the database branch to be deleted.

    Returns:
        Parsed JSON response confirming deletion.

    Example:
        result = await delete_database_branch("br_adjb2971mcran283mc")
        # result might be:
        # {"data": {"message": "ok"}, "error": null, "successful": true}
    """
    from .client import SupabaseAPIClient

    client = SupabaseAPIClient()
    return await client.delete(f"/branches/{branch_id}")
