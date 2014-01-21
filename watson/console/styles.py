# -*- coding: utf-8 -*-
TERMINATE = '\033[0m'


def underline(string, terminate=True):
    """Underlines text within the terminal.

    Example:

    .. code-block:: python
        underline('some text')  # underlined text in terminal

    Args:
        string (string): The string to wrap
        terminate (boolean): Whether or not to terminate the styling
    """
    return format_style(string, '\033[4m', TERMINATE if terminate else '')


def bold(string, terminate=True):
    """Bolds text within the terminal.

    Example:

    .. code-block:: python
        bold('some text')  # bolded text in terminal

    Args:
        string (string): The string to wrap
        terminate (boolean): Whether or not to terminate the styling
    """
    return format_style(string, '\033[1m', TERMINATE if terminate else '')


def format_style(string, start, end=TERMINATE):
    """Formats text for usage within the terminal.

    Example:

    .. code-block:: python
        format_style('some text', 'hello ', ' world')  # hello some text world

    Args:
        string (string): The string to wrap
        terminate (boolean): Whether or not to terminate the styling
    """
    return '{0}{1}{2}'.format(start, string, end)
