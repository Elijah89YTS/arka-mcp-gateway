from typing import Any, Dict, Optional


async def create_database_branch(
    ref: str,
    branch_name: str,
    desired_instance_size: Optional[str] = None,
    git_branch: Optional[str] = None,
    persistent: Optional[bool] = None,
    postgres_engine: Optional[str] = None,
    region: Optional[str] = None,
    release_channel: Optional[str] = None
) -> Any:
    """
    Creates a new, isolated database branch from an existing Supabase project.

    Args:
        ref: The unique reference ID of the parent Supabase project.
        branch_name: A unique name for the new database branch.
        desired_instance_size: Compute instance size for the new branch.
        git_branch: Git branch name to associate with this database branch.
        persistent: True for persistent branch, False for ephemeral.
        postgres_engine: Desired PostgreSQL engine version.
        region: Geographical region for the new database branch.
        release_channel: Release channel determining feature stability.

    Returns:
        Parsed JSON response containing the created branch data.

    Example:
        result = await create_database_branch(
            ref="projectref_012345",
            branch_name="staging-branch",
            region="us-east-1",
            persistent=True
        )
        # result might be:
        # {"data": {"id": "br_xyz", "name": "staging-branch", ...}, "error": null, "successful": true}
    """
    from .client import SupabaseAPIClient

    client = SupabaseAPIClient()
    payload: Dict[str, Any] = {"name": branch_name}
    if desired_instance_size:
        payload["desired_instance_size"] = desired_instance_size
    if git_branch:
        payload["git_branch"] = git_branch
    if persistent is not None:
        payload["persistent"] = persistent
    if postgres_engine:
        payload["postgres_engine"] = postgres_engine
    if region:
        payload["region"] = region
    if release_channel:
        payload["release_channel"] = release_channel
    return await client.post(f"/projects/{ref}/branches", json_data=payload)
