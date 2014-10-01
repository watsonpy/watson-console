# -*- coding: utf-8 -*-
import argparse
from collections import OrderedDict
import os
import re
import sys
from watson.common.imports import load_definition_from_string
from watson.common.contextmanagers import suppress
from watson.console import colors, styles


USAGE_REGEX = re.compile('(\w+[\:])(.+?(?=\[))(.*)')


class Runner(object):
    """A command line runner that allows new commands to be added and run on
    demand.

    Commands can be added either as a fully qualified name, or imported.

    Example:

    .. code-block:: python

        runner = Runner(commands=['module.commands.ACommand'])
        runner()
    """
    _name = None
    _commands = None

    def __init__(self, commands=None):
        self._commands = []
        if commands:
            self.add_commands(commands)

    @property
    def name(self):
        """Returns the name of the script that runner was executed from.
        """
        return self._name

    @property
    def commands(self):
        """A list of all commands added to the runner.

        Returns:
            OrderedDict containing all the commands.
        """
        commands = {}
        for command in self._commands:
            if isinstance(command, str):
                command = load_definition_from_string(command)
            commands[command.cased_name()] = command
        return OrderedDict(sorted(commands.items()))

    def add_command(self, command):
        """Convenience method to add new commands after the runner has been
        initialized.

        Args:
            command (string|class): the command to add
        """
        self._commands.append(command)

    def add_commands(self, commands):
        """Convenience method to add multiple commands.

        Args:
            commands (list|tuple): the commands to add
        """
        for command in commands:
            self.add_command(command)

    def get_command(self, command_name):
        """Returns an initialized command from the attached commands.

        Args:
            command_name: The command name to retrieve
        """
        if command_name not in self.commands:
            return None
        return self.commands[command_name]()

    def update_usage(self, parser, namespace, is_subparser=False):
        """Updates the usage for the relevant parser.

        Forces the usage message to include the namespace and color.
        """
        usage = parser.format_usage()
        r = USAGE_REGEX.search(usage)
        if not r:
            return
        parts = [s for s in r.groups()]
        if namespace:
            if is_subparser:
                method_part = parts[1].split(' ')
                method_part.insert(-2, namespace)
                parts[1] = ' '.join(method_part)
            else:
                parts.insert(2, '{} '.format(namespace))
        parser.usage = colors.header(''.join(parts[1:]).strip())

    def attach_commands(self, parser, namespace):
        """Register the commands against the parser.

        Args:
            parser: The parser to add commands to
            namespace: The namespace the commands should sit within
        """
        subparsers = parser.add_subparsers()
        namespaces = {}
        for command_class in self.commands:
            command_class = self.get_command(command_class)
            command_namespace = command_class.cased_name()
            if command_namespace not in namespaces:
                namespaces[command_namespace] = []
            command_help = command_class.help()
            # if namespace in self.commands:
            methods = [cmethod for cmethod in dir(command_class)
                       if hasattr(getattr(command_class, cmethod), 'is_cli_command')]
            for a_command in methods:
                command = getattr(command_class, a_command)
                namespaces[command_namespace].append((a_command, command.__func_doc__))
                if command_namespace == namespace:
                    subparser = subparsers.add_parser(
                        a_command,
                        help=command.__func_doc__,
                        description=command.__desc__)
                    for arg, kwargs in command.__args__:
                        subparser.add_argument(arg, **kwargs)
                    subparser.set_defaults(
                        command=(
                            command_class,
                            a_command,
                            command.__args_mapping__))
                    self.update_usage(
                        subparser, namespace, is_subparser=True)
            if command_namespace == namespace:
                # when viewing a command
                parser.description = command_help
                self.update_usage(parser, namespace)
                return
            if not namespace:
                # when viewing the namespaces
                subparsers.add_parser(
                    command_namespace,
                    description=command_help,
                    help=command_help)
        self.update_usage(parser, namespace)
        if not namespace or namespace not in namespaces:
            # Override the default output from argparse to display all the
            # namespaces and their commands.
            parser.print_usage()
            self.write()
            longest_namespace = max(namespaces, key=len)
            length = len(longest_namespace)
            for namespace in sorted(namespaces):
                commands = namespaces[namespace]
                self.write(colors.fail(styles.bold(namespace.ljust(length))))
                longest_command = max([command[0] for command in commands], key=len)
                longest_command_length = len(longest_command)
                for command, help in sorted(commands):
                    command = styles.bold(command.ljust(longest_command_length))
                    self.write('    {}\t{}'.format(command, help))
                self.write()
            sys.exit(0)

    def write(self, message=''):
        sys.stdout.write(message + '\n')

    def execute(self, args):
        """Execute the runner and any commands the user has specified.
        """
        if not args:
            args = sys.argv[:]
        self._name = os.path.basename(args.pop(0))
        execute = True
        help = '-h'
        method = help
        namespace = None
        # Always show help if invalid command
        try:
            namespace, method, *_ = args
        except:
            with suppress(Exception):
                namespace = args[0]
            execute = False
            args.append(method)
        if namespace:
            args = args[1:]
        if namespace == help:
            namespace = None

        # Add the relevant commands
        parser = argparse.ArgumentParser()
        try:
            self.attach_commands(parser, namespace)
        except ConsoleError as exc:
            self._handle_exc(exc)

        # Parse the input
        parsed_args = parser.parse_args(args)
        if execute:
            instance, method, args = parsed_args.command
            try:
                kwargs = {arg_name: getattr(parsed_args, arg_name)
                          for attr, arg_name in args.items()}
                return getattr(instance, method)(**kwargs)
            except ConsoleError as exc:
                self._handle_exc(exc)

    def _handle_exc(self, exc):
        exc_msg = str(exc).strip("'")
        sys.stderr.write(colors.fail('Error: {0}\n'.format(exc_msg)))
        sys.exit(1)

    def __call__(self, args=None):
        # Convenience to execute()
        return self.execute(args)


class ConsoleError(KeyError):
    """An error that should be raised from within the command.
    """
