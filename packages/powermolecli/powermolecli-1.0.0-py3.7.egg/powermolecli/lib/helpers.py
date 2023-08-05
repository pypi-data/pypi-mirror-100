#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: helpers.py
#
# Copyright 2021 Vincent Schouten
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.
#

"""
Import all parts from helpers here.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html
"""
import logging.config
from time import sleep
from powermolelib import (Configuration,
                          start_application)
from powermolelib.powermolelibexceptions import InvalidConfigurationFile
from ..powermolecliexceptions import SetupFailed

__author__ = '''Vincent Schouten <inquiry@intoreflection.co>'''
__docformat__ = '''google'''
__date__ = '''12-05-2020'''
__copyright__ = '''Copyright 2021, Vincent Schouten'''
__license__ = '''MIT'''
__maintainer__ = '''Vincent Schouten'''
__email__ = '''<inquiry@intoreflection.co>'''
__status__ = '''Development'''  # "Prototype", "Development", "Production".


# This is the main prefix used for logging.
logging.basicConfig(format='%(asctime)s %(name)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
LOGGER_BASENAME = '''helpers'''
LOGGER = logging.getLogger(LOGGER_BASENAME)  # non-class objects like functions can consult this Logger object
# LOGGER.addHandler(logging.NullHandler())  # method not in https://docs.python.org/3/library/logging.html


def parse_config_file(config_file_path):
    """Parses the configuration file to a (dictionary) object."""
    try:
        configuration = Configuration(config_file_path)
        LOGGER.debug('Gateways: %s', configuration.gateways)
        LOGGER.debug('Destination: %s', configuration.destination)
        LOGGER.debug('Forwarders: %s', configuration.forwarders_string)
    except InvalidConfigurationFile:
        return None
        # raise SystemExit(1)  # to keep it 'consistent' w/ develop design (powermolegui), no SystemExit() can be raised
    if configuration.mode == 'FOR':
        LOGGER.info('mode FOR enabled')
    elif configuration.mode == 'TOR':
        LOGGER.info('mode TOR enabled')
    elif configuration.mode == 'PLAIN':
        LOGGER.info('mode PLAIN enabled')
    return configuration


def show_menu(config, instructor):  # pylint: disable=too-many-branches
    """Shows a number of options.

    Most of these options invoke methods in the Instructor().

    """
    menu = {'1.': "Send commands",
            '2.': "Send files",
            '3.': "Start application stated in configuration file",
            '4.': "Quit (or control + c)"}
    while True:
        options = menu.keys()
        for entry in options:
            print(entry, menu[entry])

        selection = input(">  please select: ")[-1]  # to exclude the Space (and or other) character
        if selection == '1':
            while True:
                command = input('>  enter command: ')
                response_raw = instructor.send_command(command)
                response_str = response_raw.decode("utf-8")
                response_line = response_str.split('\n')
                for line in response_line:
                    print('%s' % line)
        elif selection == '2':
            while True:
                source_file = input('> enter source path + file name:')
                destination_path = input('> enter destination path on destination host:')
                instructor.send_file(source_file.strip(), destination_path.strip())
        elif selection == '3':
            try:
                process = start_application(binary_name=config.application['binary_name'],
                                            binary_location=config.application['binary_location'])
            except TypeError:
                LOGGER.error('something went wrong starting the application or the application was not in file')
                return
            try:
                while True:
                    sleep(1)
            except KeyboardInterrupt:
                process.terminate()
                return
        elif selection == '4':
            break
        else:
            print("Unknown Option Selected!")


def setup_link(state, transfer_agent, tunnel, bootstrap_agent,   # pylint: disable=too-many-arguments
               instructor, debug=None):  # pylint: disable=unused-argument
    """Establishes a connection to target destination host via intermediaries by starting various objects.

    This function also passes the instantiated objects to the StateManager, which
    will stop the Tunnel and Instructor after a KeyboardInterrupt (by the user
    or by the program (in COMMAND and FILE mode)).

    Args:
        state (StateManager): An instantiated StateManager object.
        transfer_agent (TransferAgent): An instantiated TransferAgent object.
        tunnel (Tunnel): An instantiated Tunnel object.
        bootstrap_agent (BootstrapAgent): An instantiated BootstrapAgent object.
        instructor (Instructor): An instantiated Assistant object.
        debug(bool): if True enable debugging mode

    """
    if not transfer_agent.start():
        raise SetupFailed(transfer_agent)
    LOGGER.info('Agent has been transferred securely to destination host')

    state.add_object(tunnel)
    if not tunnel.start(debug=False):
        raise SetupFailed(tunnel)
    LOGGER.info('Tunnel has been opened...')

    # the BootstrapAgent object is a disposable one-trick pony
    if not bootstrap_agent.start():
        raise SetupFailed(bootstrap_agent)
    LOGGER.info('Agent has been executed')

    state.add_object(instructor)
    if not instructor.start():
        raise SetupFailed(instructor)
    LOGGER.info('Instructor has been executed')
