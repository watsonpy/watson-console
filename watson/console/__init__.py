# -*- coding: utf-8 -*-
__version__ = '1.0.1'

try:
    # Fix for setup.py version import
    from watson.console.runner import Runner, ConsoleError

    __all__ = ['Runner', 'ConsoleError']
except:  # pragma: no cover
    pass  # pragma: no cover
