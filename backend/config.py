"""Application configuration using Dynaconf.

This module provides centralized configuration management using Dynaconf.
Settings are loaded from environment variables, .env files, and settings files.

Example:
    Access settings in your code::

        from config import settings

        print(settings.JWT_SECRET_KEY)
        print(settings.JWT_ALGORITHM)
        print(settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)

Environment Variables:
    JWT_SECRET_KEY: Secret key for signing JWT tokens
    JWT_ALGORITHM: Algorithm for JWT signing (default: HS256)
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: Access token expiration in minutes (default: 30)
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: Refresh token expiration in days (default: 7)
"""
import logging
import sys
from pathlib import Path
from dynaconf import Dynaconf

logger = logging.getLogger(__name__)

settings = Dynaconf(
    envvar_prefix="ARKA",  # Export variables as ARKA_VAR_NAME
    settings_files=["settings.toml", ".secrets.toml"],
    environments=True,  # Enable layered environments (dev, staging, prod)
    env_switcher="ENV_FOR_DYNACONF",  # Switch environment with this var
    load_dotenv=True,  # Load from .env file
    merge_enabled=True,  # Merge settings from multiple sources
)


# Enterprise Edition Detection with Submodule Support
# ---------------------------------------------------
def _setup_enterprise_path():
    """
    Set up enterprise module path from submodule if available.

    This checks for the enterprise submodule and adds it to sys.path
    BEFORE trying to import, so Python will find the real enterprise
    implementation instead of the stubs.

    This enables all enterprise features including:
    - Azure SSO authentication
    - Per-user tool permissions
    - And any future enterprise features
    """
    # Path to enterprise submodule: ../enterprise/backend/
    backend_dir = Path(__file__).parent  # /path/to/arka-mcp-gateway/backend
    repo_root = backend_dir.parent       # /path/to/arka-mcp-gateway
    enterprise_submodule_backend = repo_root / "enterprise" / "backend"

    # Check if submodule exists and has enterprise module
    enterprise_init = enterprise_submodule_backend / "enterprise" / "__init__.py"

    if enterprise_init.exists():
        # Add submodule backend to sys.path so imports resolve there first
        # This gives the enterprise implementation priority over community stubs
        # Security note: This is safe because the enterprise submodule is
        # a trusted repository controlled by KenisLabs
        submodule_path_str = str(enterprise_submodule_backend)
        if submodule_path_str not in sys.path:
            sys.path.insert(0, submodule_path_str)
            logger.info(f"Enterprise submodule detected, added to path: {submodule_path_str}")
            return True

    return False


# Set up enterprise path before any enterprise imports
_enterprise_submodule_available = _setup_enterprise_path()


def is_enterprise_edition() -> bool:
    """
    Check if this is the enterprise edition.

    Detection order:
    1. Check if enterprise submodule exists (via _setup_enterprise_path)
    2. Try to import enterprise.__enterprise__ marker
    3. Return True only if marker is True (stubs have __enterprise__ = False)

    Returns:
        bool: True if running enterprise edition, False for community edition
    """
    try:
        from enterprise import __enterprise__
        return __enterprise__ is True  # Stubs have __enterprise__ = False
    except (ImportError, AttributeError):
        return False


def get_enterprise_module(module_name: str):
    """
    Dynamically import enterprise module if available.

    Args:
        module_name: Module path relative to enterprise package (e.g., "auth.azure")

    Returns:
        Module object if successful, None otherwise
    """
    if not is_enterprise_edition():
        return None

    try:
        import importlib
        return importlib.import_module(f"enterprise.{module_name}")
    except ImportError as e:
        logger.error(f"Failed to import enterprise.{module_name}: {e}")
        return None
