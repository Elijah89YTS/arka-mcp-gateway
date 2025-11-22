from typing import Any, Optional, Dict

async def deploy_function(
    ref: str,
    slug: Optional[str] = None,
    file_content: Optional[str] = None,
    file_url: Optional[str] = None,
    file: Optional[Dict[str, Any]] = None,
    bundleOnly: Optional[bool] = None
) -> Any:
    """
    Deploys Edge Functions to a Supabase project.

    Supports multipart or JSON payloads for code upload or references.

    Args:
        ref: Supabase project reference ID.
        slug: Optional slug of the function to deploy; omit to deploy all in bundle.
        file_content: Raw source code string for simple functions.
        file_url: Public URL to download function code.
        file: File upload descriptor (mimetype, name, s3key) for large or binary bundles.
        bundleOnly: If true, only bundle the function without publishing.

    Returns:
        Parsed JSON response with deployment results per function.

    Example:
        result = await deploy_function(
            ref="projectref_abc123",
            slug="send-email",
            file_url="https://example.com/function.zip"
        )
    """
    from .client import SupabaseAPIClient

    client = SupabaseAPIClient()
    payload: Dict[str, Any] = {}
    if slug is not None:
        payload["slug"] = slug
    if file_content is not None:
        payload["file_content"] = file_content
    if file_url is not None:
        payload["file_url"] = file_url
    if file is not None:
        payload["file"] = file
    if bundleOnly is not None:
        payload["bundleOnly"] = bundleOnly
    return await client.post(f"/projects/{ref}/functions/deploy", json_data=payload)
