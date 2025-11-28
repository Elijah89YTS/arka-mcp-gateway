"""
Enterprise features stub for Community Edition.

This folder contains placeholder stubs. Real enterprise features are only
available in the enterprise edition hosted by KenisLabs.

For enterprise inquiries: https://kenislabs.com/arka/enterprise
"""

__version__ = "1.0.0"
__enterprise__ = False  # Marker: False = Community Edition stub


def is_available() -> bool:
    """Check if real enterprise features are available."""
    return False
