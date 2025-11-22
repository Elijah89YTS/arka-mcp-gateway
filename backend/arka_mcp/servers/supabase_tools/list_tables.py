from typing import Any, Dict, List, Optional

from .run_sql_query import run_sql_query

async def list_tables(
    ref: str,
    include_metadata: bool = True,
    include_system_schemas: bool = False,
    include_views: bool = True,
    schemas: Optional[List[str]] = None
) -> Any:
    """
    Lists all tables and views in specified database schemas.

    LLM Guidance: Use this tool for listing database tables/views instead of run_sql_query
    when the user asks to list tables in a project.

    Executes SQL against information_schema and pg_catalog to provide
    an overview of tables and views, including optional metadata.

    Args:
        ref: The unique reference ID of the Supabase project.
        include_metadata: Ignored; present for compatibility.
        include_system_schemas: Ignored; present for compatibility.
        include_views: Ignored; present for compatibility.
        schemas: Optional list of schema names to limit the search.

    Returns:
        A dict matching the ListTablesResponseWrapper schema:
        {
          "data": {
            "schemas": [
              {
                "schema_name": "public",
                "tables": [
                  {"table_name": ..., "full_name": ..., ...},
                  ...
                ],
                "table_count": <int>,
                "view_count": <int>
              }, ...
            ],
            "query_metadata": {...},
            "total_schemas": <int>,
            "total_tables": <int>,
            "total_views": <int>
          },
          "error": None,
          "successful": True
        }

    Example:
        result = await list_tables(ref="projectref_0123456789abcdef")
    """
    # Query basic list of tables/views
    sql = (
        "SELECT table_schema, table_name, table_type "
        "FROM information_schema.tables "
        f"WHERE table_schema NOT IN ('pg_catalog', 'information_schema') "
        "ORDER BY table_schema, table_name;"
    )
    resp = await run_sql_query(ref=ref, query=sql)
    # SQL endpoint returns list of row dicts, no wrapper
    rows = resp if isinstance(resp, list) else (resp.get('data') or [])
    # Organize by schema
    schema_map: Dict[str, Dict[str, Any]] = {}
    total_tables = 0
    total_views = 0
    for row in rows:
        sch = row.get('table_schema')
        typ = row.get('table_type')
        entry = schema_map.setdefault(sch, {
            'schema_name': sch,
            'tables': [],
            'table_count': 0,
            'view_count': 0
        })
        entry['tables'].append({
            'table_name': row.get('table_name'),
            'full_name': f"{sch}.{row.get('table_name')}",
            'table_type': typ
        })
        if typ == 'BASE TABLE':
            entry['table_count'] += 1
            total_tables += 1
        else:
            entry['view_count'] += 1
            total_views += 1
    schemas_list: List[Dict[str, Any]] = list(schema_map.values())
    return {
        'data': {
            'query_metadata': {
                'include_metadata': include_metadata,
                'include_views': include_views,
                'errors': None
            },
            'schemas': schemas_list,
            'tables': None,
            'total_schemas': len(schemas_list),
            'total_tables': total_tables,
            'total_views': total_views
        },
        'error': None,
        'successful': True
    }
