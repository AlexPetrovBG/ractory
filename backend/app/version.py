"""Version information for Ra Factory API."""

__version__ = "0.1.0"
__api_version__ = "v1"

def get_version_info():
    """Return version information dictionary."""
    return {
        "version": __version__,
        "api_version": __api_version__
    } 