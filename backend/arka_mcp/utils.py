import importlib
import inspect
import logging

logger = logging.getLogger(__name__)


def parse_tool_file(module_name: str, service: str, tool: str):
    """
    Dynamically imports the tool function and extracts structured metadata.

    Returns None if the module or function does not exist.

    Output format:
    {
        "tool_ref": "jira_tools.search_issues",
        "function_name": "search_issues",
        "signature": "(jql: str, max_results: int = 20, fields: list[str] | None = None)",
        "docstring": "...",
        "return_type": "dict",
        "decorators": [],   # best effort
        "category": "jira"
    }
    """

    try:
        module = importlib.import_module(module_name)
    except ModuleNotFoundError as e:
        logger.warning(
            f"Tool module not found: {module_name} "
            f"(service={service}, tool={tool}). Error: {e}"
        )
        return None
    except ImportError as e:
        logger.error(
            f"Failed to import tool module: {module_name} "
            f"(service={service}, tool={tool}). Error: {e}"
        )
        return None
    except Exception as e:
        logger.error(
            f"Unexpected error importing module: {module_name}. "
            f"Error: {type(e).__name__}: {e}"
        )
        return None

    try:
        func = getattr(module, tool)
    except AttributeError as e:
        logger.warning(
            f"Tool function '{tool}' not found in module {module_name}. Error: {e}"
        )
        return None

    # Signature string
    signature = str(inspect.signature(func))

    # Docstring
    docstring = inspect.getdoc(func)

    # Return type
    sig = inspect.signature(func)
    return_type = None
    if sig.return_annotation is not inspect.Signature.empty:
        return_type = sig.return_annotation

    # Decorators (best-effort; requires `@wraps` usage to be visible)
    decorators = []
    if hasattr(func, "__wrapped__"):
        decorators.append(func.__wrapped__.__name__)

    return {
        "tool_ref": module_name,
        "function_name": func.__name__,
        "signature": signature,
        "docstring": docstring,
        "return_type": str(return_type) if return_type else None,
        "decorators": decorators,
        "category": service,
    }
