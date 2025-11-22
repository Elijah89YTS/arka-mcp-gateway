from typing import Any, List, Dict

from .run_sql_query import run_sql_query

async def get_table_schemas(
    ref: str,
    table_names: List[str],
    include_indexes: bool = True,
    include_relationships: bool = True,
    exclude_null_values: bool = True
) -> Any:
    """
    Retrieves column and basic schema information for specified tables.

    LLM Guidance: Use this tool for table schema introspection instead of run_sql_query
    when the user asks for table schemas.

    Executes SQL queries against the project's database to fetch column metadata
    for each table in `table_names`. This function returns a simplified schema
    output since Supabase Management API does not support a dedicated schema endpoint.

    Args:
        ref: The unique reference ID of the Supabase project.
        table_names: List of table names, optionally prefixed by schema (e.g., 'public.users').
        include_indexes: Ignored; present for compatibility.
        include_relationships: Ignored; present for compatibility.
        exclude_null_values: Ignored; present for compatibility.

    Returns:
        A dict matching the GetTableSchemasResponseWrapper schema:
        {
          "data": {
            "tables": [
              {
                "schema": "public",
                "table": "users",
                "columns": [
                  {"column_name": ..., "data_type": ..., ...},
                  ...
                ]
              }, ...
            ],
            "total_found": <int>,
            "total_requested": <int>
          },
          "error": None,
          "successful": True
        }

    Example:
        result = await get_table_schemas(
            ref="projectref_0123456789abcdef",
            table_names=["users", "public.posts"]
        )
    """
    tables: List[Dict[str, Any]] = []
    for full_name in table_names:
        if "." in full_name:
            schema, table = full_name.split('.', 1)
        else:
            schema, table = 'public', full_name
        # Query column metadata from information_schema
        sql = (
            "SELECT column_name, data_type, is_nullable, column_default "
            "FROM information_schema.columns "
            f"WHERE table_schema = '{schema}' AND table_name = '{table}' "
            "ORDER BY ordinal_position;"
        )
        resp = await run_sql_query(ref=ref, query=sql)
        # Extract rows: SQL endpoint returns list of row dicts
        cols = resp if isinstance(resp, list) else (resp.get('data') or [])
        tables.append({
            "schema": schema,
            "table": table,
            "columns": cols
        })
    return {
        "data": {
            "tables": tables,
            "total_found": len(tables),
            "total_requested": len(table_names)
        },
        "error": None,
        "successful": True
    }
