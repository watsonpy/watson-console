# -*- coding: utf-8 -*-
from pytest import raises
from watson.console.command import Base, find_commands_in_module
from tests.watson.console import support


class TestBaseCommand(object):

    def test_init(self):
        with raises(TypeError):
            Base()


class TestFindCommands(object):

    def test_find_commands(self):
        commands = find_commands_in_module(support)
        assert len(commands) == 7
