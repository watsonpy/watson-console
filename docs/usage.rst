Usage
=====

Commands in Watson are broken down into three parts, SCRIPT NAMESPACE ARGUMENTS. The script refers to the file that the user needs to call to execute the command (this usually refers to *console.py*). The namespace is the location that the command resides in, allowing console commands to be split into different functional areas. Arguments are what the user can pass to the command to modify it's behaviour.

An example command from watson.framework is `new`, which resides in the `project` namespace. It also contains several arguments, `dir` and `override`. The command itself looks like:

.. code-block:: bash

    console.py project new [--dir DIR] [--override] name app_name

The anatomy of a command
------------------------

.. code-block:: python

   # can be executed by `script.py my_namespace method`
   from watson.console import command
   from watson.console.decorators import arg

   class MyNamespace(command.Base):
        help = 'Displayed when script.py my_namespace -h is called'
        name = 'my_namespace'  # if not defined, a snake_case version of the class name will be used

        @arg()
        def method(self):
            """Command specific help, printed when -h is called

            More information about the command.
            """
            print('Run!')

        @arg()
        def another(self, positional):
            """Help...

            Args:
                positional: The positional argument help string
            """


Defining arguments
------------------

Whenever a command is executed, any arguments that are passed to it will also be passed to the associated method.

The @arg decorator also takes any kwargs that the ``add_argument`` method from argparse has (see https://docs.python.org/3/library/argparse.html).

Positional
^^^^^^^^^^

Positional arguments can be defined in two ways, either using the @arg decorator, or by just adding the name as argument to the method.

.. code-block:: python

    # imports...

    class MyCommand(command.Base):
        # help, name etc...

        @arg()
        def method(self, positional):
            """The command help

            Args:
                positional: The positional argument help string
            """

        @arg('positional')
        def another(self, **kwargs)
            """Help

            Args:
                positional: The help string
            """


Optional
^^^^^^^^

Optional arguments are also created in the same way that positional arguments are, except that they take an additional optional=True argument. The name of the argument must also be defined in the @arg decorator.

.. code-block:: python

    # imports...

    class MyCommand(command.Base):
        # help, name etc...

        @arg('optional', optional=True)
        def method(self, optional):
            """The command help

            Args:
                optional: The optional argument help string
            """

Using the command in your app
-----------------------------

Within your application config, simply create a new definition named ``commands``. Assuming the above command is within the ``myapp.commands`` module, the definition would look like this:

.. code-block:: python

    # within config.py
    from watson.console.command import find_commands_in_module
    from myapp import commands

    commands = find_commands_in_module(commands)
