#!/usr/bin/env python
# flake8: noqa: E402,F401
__version__ = '0.6.0.dev2'

try:
    from .response import AnyResponse, CachedHTTPResponse, CachedResponse, ExpirationTime
    from .core import (
        ALL_METHODS,
        CachedSession,
        CacheMixin,
        clear,
        disabled,
        enabled,
        get_cache,
        install_cache,
        is_installed,
        remove_expired_responses,
        uninstall_cache,
    )
# Quietly ignore ImportError, if setup.py is invoked outside a virtualenv
except ImportError:
    pass
