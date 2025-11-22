from typing import Any

async def list_all_database_backups(ref: str) -> Any:
    """
    Lists all database backups for a Supabase project.

    Retrieves details on all backups (physical snapshots and PITR metadata)
    via the Supabase Management API `/v1/projects/{ref}/database/backups`.

    Args:
        ref: The unique reference ID of the Supabase project.

    Returns:
        Parsed JSON response containing backup metadata, including:
          - `data.backups`: list of backup entries
          - `data.physical_backup_data`: available PITR range
          - `data.pitr_enabled`, `data.walg_enabled`, `data.region`
    Example:
        result = await list_all_database_backups(
            ref="projectref_0123456789abcdef"
        )
        # result might be:
        # {
        #   "data": {
        #     "backups": [{"inserted_at": "...", "status": "COMPLETED", "is_physical_backup": true}],
        #     "physical_backup_data": {"earliest_physical_backup_date_unix": 1678886400, "latest_physical_backup_date_unix": 1678972800},
        #     "pitr_enabled": true,
        #     "walg_enabled": true,
        #     "region": "us-east-1"
        #   },
        #   "error": null,
        #   "successful": true
        # }
    """
    from .client import SupabaseAPIClient

    client = SupabaseAPIClient()
    # Call Supabase Management API to list backups
    return await client.get(f"/projects/{ref}/database/backups")
