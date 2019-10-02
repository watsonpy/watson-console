# -*- coding: utf-8 -*-
__version__ = '2.0.4'

try:
    # Fix for setup.py version import
    from watson.console.runner import Runner, ConsoleError

    __all__ = ['Runner', 'ConsoleError']
except:  # noqa, pragma: no cover
    pass  # pragma: no cover
