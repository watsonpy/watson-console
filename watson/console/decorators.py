# -*- coding: utf-8 -*-
import functools
import inspect
import re
from watson.common.contextmanagers import suppress

__all__ = ['arg', 'cmd']

DOC_REGEX = re.compile('(?P<arg>\w+)(|.)+[\:]\ (?P<help>.*)', re.MULTILINE)


def _ensure_func_attrs(func):
    """Add the relevant attributes to the function.
    """
    if not hasattr(func, '__args__'):
        func.__args__ = []
        func.__args_mapping__ = {}


class arg(object):
    """Adds arguments to a command.

    To define optional arguments (--optional) an additional optional=True kwarg
    can be specified. Leaving the kwargs blank will force the method to be
    treated as a command.

    Example:

    .. code-block:: python

        class MyCommand(Base):
            @arg('name')
            def method(self, name):
                '''The one line help for the command.

                The full description that's displayed when using -h

                Args:
                    name: An additional argument
                '''
                print('Executed', name)  # Executed [name]

    """
    name = None
    base_command = False
    optional = False

    def __init__(self, name=None, **kwargs):
        self.name = name
        if 'optional' in kwargs:
            self.optional = True
            del kwargs['optional']
        self.kwargs = kwargs
        self.validate_name(name)

    def add_func_to_arg_list(self, func, name, prefixed_name):
        index = None
        try:
            index = [arg[0] for arg in func.__args__].index(prefixed_name)
        except:
            with suppress(Exception):
                idx = [arg[0] for arg in func.__args__].index(name)
                del func.__args__[idx]
            func.__args__.append((prefixed_name, self.kwargs))
        if index:
            func.__args__[index] = (self.arg_name, self.kwargs)

    def process_docstring(self, func):
        if not hasattr(func, '__func_doc__'):
            doc = func.__doc__ or 'Missing doc.'
            lines = doc.splitlines()
            kw = self.kwargs
            func.__func_doc__ = kw['help'] if 'help' in kw else lines[0]
            description = []
            for line in lines:
                line = line.strip()
                if line.startswith('Args:'):
                    break
                description.append(line)
            if description:
                func.__desc__ = '\n'.join(description)
            else:
                func.__desc__ = func.__func_doc__
            func.help = {k: v for k, t, v in DOC_REGEX.findall(doc)}

    def validate_name(self, name):
        if not self.name:
            self.name = name
            if not self.kwargs:
                self.base_command = True

    def __call__(self, func):
        self.validate_name(func.__name__)
        self.process_docstring(func)
        _ensure_func_attrs(func)

        if 'help' not in self.kwargs:
            self.kwargs['help'] = func.help.get(self.name, '')
        if not hasattr(func, 'is_cli_command'):
            # Add any named arguments, we'll override them later if the
            # arg has been specified in a decorator
            spec = inspect.getargspec(func)
            for arg in spec[0][1:]:
                func.__args_mapping__[arg] = arg
                func.__args__.append((arg, {'help': func.help.get(arg, '')}))
        func.is_cli_command = True

        if not self.base_command:
            func.__args_mapping__[self.arg_name] = self.name
            self.add_func_to_arg_list(func, self.name, self.arg_name)

        @functools.wraps(func)
        def decorated(*args, **kwargs):
            return func(*args, **kwargs)
        return decorated

    @property
    def arg_name(self):
        if self.optional:
            return '{}{}'.format('--', self.name)
        return self.name


class cmd(arg):
    """To be used for semantic purposes if the command has no arguments.
    """
