from typing import Any, Dict, Optional


async def create_project(
    db_pass: str,
    name: str,
    organization_id: str,
    region: str,
    desired_instance_size: Optional[str] = None,
    kps_enabled: Optional[bool] = None,
    plan: Optional[str] = None,
    postgres_engine: Optional[str] = None,
    release_channel: Optional[str] = None,
    template_url: Optional[str] = None
) -> Any:
    """
    Creates a new Supabase project under the specified organization.

    Args:
        db_pass: Password for the new database.
        name: Unique name for the project (no dots).
        organization_id: Identifier of the organization (slug or ID).
        region: Cloud region for hosting the project.
        desired_instance_size: Optional compute instance size.
        kps_enabled: Deprecated; ignored.
        plan: Subscription plan (ignored in request).
        postgres_engine: Optional PostgreSQL engine version.
        release_channel: Optional release channel for feature stability.
        template_url: Optional URL for a project template to initialize.

    Returns:
        Parsed JSON response containing the created project data.

    Example:
        result = await create_project(
            db_pass="S3cur3P@ss!",
            name="my-awesome-app",
            organization_id="my-cool-org",
            region="us-east-1",
            plan="free"
        )
        # result might be:
        # {"data": {"id": "proj_abc", "name": "my-awesome-app", ...}, "error": null, "successful": true}
    """
    from .client import SupabaseAPIClient

    client = SupabaseAPIClient()
    payload: Dict[str, Any] = {
        "db_pass": db_pass,
        "name": name,
        "organization_id": organization_id,
        "region": region
    }
    if desired_instance_size:
        payload["desired_instance_size"] = desired_instance_size
    if kps_enabled is not None:
        payload["kps_enabled"] = kps_enabled
    if plan:
        payload["plan"] = plan
    if postgres_engine:
        payload["postgres_engine"] = postgres_engine
    if release_channel:
        payload["release_channel"] = release_channel
    if template_url:
        payload["template_url"] = template_url
    # Endpoint: POST /v1/projects
    return await client.post("/projects", json_data=payload)
