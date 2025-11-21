from typing import Any


async def run_sql_query(ref: str, query: str) -> Any:
    """
    Executes a given SQL query against the Supabase project’s database.

    Use for advanced data operations or when standard API endpoints are insufficient.

    Args:
        ref: The unique reference ID of the Supabase project.
        query: The SQL query to be executed against the project’s database.

    Returns:
        Parsed JSON response from the Supabase management API, typically containing query results or confirmation of execution.

    Example:
        # Select rows
        result = await run_sql_query(
            ref="projectref_0123456789abcdef",
            query="SELECT * FROM users WHERE id = 1;"
        )
        # result might be:
        # {"data": [{"id": 1, "email": "user@example.com", ...}], "error": null, "successful": true}

        # Insert row
        result = await run_sql_query(
            ref="projectref_0123456789abcdef",
            query="INSERT INTO products (name, price) VALUES ('New', 9.99);"
        )
    """
    from .client import SupabaseAPIClient

    client = SupabaseAPIClient()
    # Execute SQL query via management API
    payload = {"query": query}
    return await client.post(f"/projects/{ref}/database/query", json_data=payload)
