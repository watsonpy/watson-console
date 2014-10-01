# -*- coding: utf-8 -*-
from watson.console.command import find_commands_in_module
from tests.watson.console import support


class TestFindCommands(object):

    def test_find_commands(self):
        commands = find_commands_in_module(support)
        assert len(commands) == 7
