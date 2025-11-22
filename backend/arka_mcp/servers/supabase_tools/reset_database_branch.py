from typing import Any


async def reset_database_branch(branch_id: str) -> Any:
    """
    Resets an existing Supabase database branch to its initial clean state, deleting all data and schema changes.

    Args:
        branch_id: The unique identifier of the database branch to reset.

    Returns:
        Parsed JSON response confirming reset.

    Example:
        result = await reset_database_branch("br_123abc456def")
        # result might be:
        # {"data": {"message": "ok", "workflow_run_id": "wr_789"}, "error": null, "successful": true}
    """
    from .client import SupabaseAPIClient

    client = SupabaseAPIClient()
    # Execute branch reset
    return await client.post(f"/branches/{branch_id}/reset", json_data={})
