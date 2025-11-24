"""
Script to clear OAuth provider cache for github-mcp.
This forces the provider to reload credentials from database on next request.
"""
import asyncio
from gateway.auth_providers.registry import get_oauth_provider_registry

def clear_cache():
    print("=== Clear GitHub MCP OAuth Provider Cache ===\n")

    registry = get_oauth_provider_registry()

    # Clear the cache for github-mcp
    registry.clear_provider_cache('github-mcp')

    print("✅ OAuth provider cache cleared for github-mcp")
    print("\nNext authorization request will load fresh credentials from database.")

if __name__ == "__main__":
    clear_cache()
