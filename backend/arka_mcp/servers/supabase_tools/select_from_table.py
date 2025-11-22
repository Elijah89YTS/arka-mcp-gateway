from typing import Any, List, Optional, Dict, Union

from .run_sql_query import run_sql_query

async def select_from_table(
    project_ref: str,
    table: str,
    select: str,
    filters: Optional[List[Dict[str, Union[str, List[Any]]]]] = None,
    order: Optional[str] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> Any:
    """
    Selects rows from a PostgREST table via SQL under the hood.

    Constructs a SQL SELECT query with optional filtering, sorting, and pagination,
    then executes it against the project's database.

    Args:
        project_ref: Unique reference ID of the Supabase project.
        table: Table or view name to select from (optionally schema-qualified).
        select: Comma-separated list of columns or JSON selectors to return.
        filters: Optional list of filter dicts: {column, operator, value}.
        order: Optional ordering string, e.g., 'created_at.desc' or 'id.asc'.
        limit: Optional max number of rows to return.
        offset: Optional number of rows to skip before returning.

    Returns:
        A dict matching SelectFromTableResponseWrapper:
        {
          "data": {"rows": [...]},
          "error": null,
          "successful": true
        }

    Example:
        result = await select_from_table(
            project_ref="proj123",
            table="public.users",
            select="id,name,email",
            filters=[{"column":"id","operator":"gt","value":100}],
            order="created_at.desc",
            limit=10
        )
    """
    # Build SQL
    where_clauses = []
    if filters:
        op_map = {
            'eq': '=', 'neq': '<>', 'gt': '>', 'gte': '>=', 'lt': '<', 'lte': '<=',
            'like': 'LIKE', 'ilike': 'ILIKE', 'is': 'IS', 'in': 'IN'
        }
        for f in filters:
            col = f['column']
            op = f['operator']
            val = f['value']
            sql_op = op_map.get(op)
            if not sql_op:
                raise ValueError(f"Unsupported operator: {op}")
            if op == 'in' and isinstance(val, (list, tuple)):
                vals = ','.join(f"'{v}'" if isinstance(v, str) else str(v) for v in val)
                clause = f"{col} IN ({vals})"
            else:
                literal = f"'{val}'" if isinstance(val, str) else str(val)
                clause = f"{col} {sql_op} {literal}"
            where_clauses.append(clause)
    where_sql = (' WHERE ' + ' AND '.join(where_clauses)) if where_clauses else ''
    order_sql = ''
    if order:
        col, _, dir = order.partition('.')
        dir = 'DESC' if dir.lower() == 'desc' else 'ASC'
        order_sql = f" ORDER BY {col} {dir}"
    limit_sql = f" LIMIT {limit}" if limit is not None else ''
    offset_sql = f" OFFSET {offset}" if offset is not None else ''
    sql = f"SELECT {select} FROM {table}{where_sql}{order_sql}{limit_sql}{offset_sql};"
    # Execute query
    resp = await run_sql_query(ref=project_ref, query=sql)
    # run_sql_query returns list of rows or dict
    rows = resp if isinstance(resp, list) else resp.get('data', [])
    return {"data": {"rows": rows}, "error": None, "successful": True}
