#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: windows.py
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
Main code for tkinter windows.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

import os
import tkinter as tk
from tkinter import DISABLED
from tkinter.filedialog import askopenfilename
import inspect
import threading
from time import sleep
from powermolegui.lib.application import application
from powermolegui.lib.frames import MainFrame, CommandFrame
from powermolegui.lib.logging import LoggerMixin
from powermolegui.lib.helpers import ItemsGenerator, parse_configuration_file

__author__ = '''Vincent Schouten <inquiry@intoreflection.co>'''
__docformat__ = '''google'''
__date__ = '''08-10-2020'''
__copyright__ = '''Copyright 2021, Vincent Schouten'''
__credits__ = ["Vincent Schouten"]
__license__ = '''MIT'''
__maintainer__ = '''Vincent Schouten'''
__email__ = '''<inquiry@intoreflection.co>'''
__status__ = '''Development'''  # "Prototype", "Development", "Production".

# Constants regarding powermole window for non-retina (generic) screens
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 500

# Constants regarding dimensions of non-retina (generic) screen
GENERIC_SCREEN_WIDTH = 1920


def determine_scale(screen_width):
    """Sets the width of the application screen depending on type of screen."""
    if screen_width <= GENERIC_SCREEN_WIDTH:
        scale = 1
    else:  # retina screen
        scale = 2
    return scale


class MainWindow(tk.Tk, LoggerMixin):
    """Represents the main window of an application.

    In an Tkinter application, the instance of the Tk class represents the main window.
    """

    def __init__(self, *args, **kwargs):
        """______________."""
        tk.Tk.__init__(self, *args, **kwargs)
        LoggerMixin.__init__(self)
        self.scale = 0
        self._set_title_icon()
        self._set_size_window()
        self._query_windowingsystem()
        self._create_menu()
        self._bind_to_event()
        self.main_frame = MainFrame(self, self.scale)
        self.main_frame.pack(side="top", fill="both", expand=True)
        self.main_frame.config(highlightthickness=2)
        self.set_scrollregion(init=True)
        self.should_terminate_powermole = False
        self.is_busy = False
        self.protocol("WM_DELETE_WINDOW", self.close_window)
        self.path_config_file = None  # the path to the config file; set by _config_file_dialog()
        self.configuration = None  # an object holding configuration parameters; set by show_config_graphics()
        self.canvas_items = None
        self.grab_set()  # prevents users from interacting with other windows

    def _determine_script_path(self):  # pylint: disable=no-self-use
        running_script = inspect.getframeinfo(inspect.currentframe()).filename
        running_script_dir = os.path.dirname(os.path.abspath(running_script))
        return running_script_dir

    def _set_title_icon(self):
        self.title("powermole")
        parent = os.path.dirname(self._determine_script_path())  # from /powermolegui/lib/ to /powermolegui/
        path_file = os.path.join(parent, 'icon', 'application_icon_tunnel.png')
        # https://stackoverflow.com/questions/11176638/tkinter-tclerror-error-reading-bitmap-file
        img = tk.PhotoImage(file=path_file)
        self.iconphoto(True, img)

    def _set_size_window(self):
        screen_width = self.winfo_screenwidth()  # width of the computer screen
        screen_height = self.winfo_screenheight()  # height of the computer screen
        self.scale = determine_scale(screen_width)
        win_width = WINDOW_WIDTH * self.scale  # width of the main window
        win_height = WINDOW_HEIGHT * self.scale  # height of the main window
        start_x = (screen_width / 2) - (win_width / 2)
        start_y = (screen_height / 2) - (win_height / 2)
        self.geometry('%dx%d+%d+%d' % (win_width, win_height, start_x, start_y))
        self.resizable(True, True)
        # self._logger.info("screen size is: %s x %s", (ws, hs))  # can't work, as logger (must) instantiate(s) later
        print("screen size is: %s x %s" % (screen_width, screen_height))
        print("window size: %s x %s" % (win_width, win_height))

    def _query_windowingsystem(self):
        print(f"windowing system: {self.tk.call('tk', 'windowingsystem')}")

    def _create_menu(self):
        self.option_add('*tearOff', False)
        menubar = tk.Menu(self)
        file_menu = tk.Menu(menubar)
        run_menu = tk.Menu(menubar)
        send_menu = tk.Menu(menubar)
        logging_menu = tk.Menu(menubar)
        quit_menu = tk.Menu(menubar)

        file_menu.add_command(label='Open', command=self._config_file_dialog)
        file_menu.entryconfig('Open', accelerator='Ctrl+O')
        file_menu.add_command(label='Open Recent', command=self._retrieve_recently_opened)
        file_menu.entryconfig('Open Recent', accelerator='Ctrl+T')
        menubar.add_cascade(label='File', menu=file_menu)

        run_menu.add_command(label='Run Powermole', command=self.run_powermole)
        run_menu.entryconfig('Run Powermole', accelerator='Ctrl+R')
        run_menu.add_command(label='Stop Powermole', command=self.stop_powermole)
        run_menu.entryconfig('Stop Powermole', accelerator='Ctrl+C')
        menubar.add_cascade(label='Execution', menu=run_menu)

        send_menu.add_command(label='Send File', command=None)
        send_menu.entryconfig('Send File', accelerator='Ctrl+F', state=DISABLED)
        send_menu.add_command(label='Send Command', command=None)
        send_menu.entryconfig('Send Command', accelerator='Ctrl+M', state=DISABLED)
        menubar.add_cascade(label='Send', menu=send_menu)

        var_info = tk.BooleanVar()
        var_info.set(value=1)
        var_debug = tk.BooleanVar()
        logging_menu.add_checkbutton(label='Info', onvalue=1, offvalue=0, variable=var_info)
        logging_menu.add_checkbutton(label='Debug', onvalue=1, offvalue=0, variable=var_debug)
        menubar.add_cascade(label='Logging', menu=logging_menu)
        logging_menu.entryconfig('Info', state='disabled')
        logging_menu.entryconfig('Debug', state='disabled')

        quit_menu.add_command(label='Quit', command=self.close_window)
        quit_menu.entryconfig('Quit', accelerator='Ctrl+Q')
        menubar.add_cascade(label='Quit', menu=quit_menu)

        self.config(menu=menubar)  # self == parent = tk.Tk()

    def _bind_to_event(self):
        self.bind('<Control-o>', lambda e: self._config_file_dialog())
        self.bind('<Control-t>', lambda e: self._retrieve_recently_opened())
        self.bind('<Control-r>', lambda e: self.run_powermole())
        self.bind('<Control-c>', lambda e: self.stop_powermole())
        self.bind('<Control-f>', lambda e: None)  # in development
        self.bind('<Control-m>', lambda e: None)  # in development
        self.bind('<Control-q>', lambda e: self.close_window())

    def set_scrollregion(self, init=False):
        """Sets a scroll region that encompasses all the shapes."""
        self.main_frame.canvas_frame.canvas_landscape.update_idletasks()
        w_height = self.main_frame.canvas_frame.canvas_landscape.winfo_height()
        w_width = self.main_frame.canvas_frame.canvas_landscape.winfo_width()
        if init:
            self.main_frame.canvas_frame.canvas_landscape.config(scrollregion=(0, 0, w_width, w_height))
        else:
            # retrieve the x-axis at the far right of the last drawn item:
            _, _, x_axis_2, _ = self.main_frame.canvas_frame.canvas_landscape.bbox('all')
            if x_axis_2 <= w_width:  # if the bounding box of all items is smaller than the canvas width,
                # dismiss bounding box size
                self.main_frame.canvas_frame.canvas_landscape.config(scrollregion=(0, 0, w_width, w_height))
            else:
                self.main_frame.canvas_frame.canvas_landscape.config(scrollregion=(0, 0, x_axis_2 + 100, w_height))

    def _retrieve_recently_opened(self):  # fix this py_lint error --> inconsistent-return-statements
        if self.is_busy:
            return None
        parent = os.path.dirname(self._determine_script_path())  # from /powermolegui/lib/ to /powermolegui/
        path_file_recent = os.path.join(parent, 'settings', 'recently_opened_config_file')
        try:
            with open(path_file_recent) as file:
                self.path_config_file = file.read().rstrip()
        except FileNotFoundError:
            return None
        config_thread = threading.Thread(target=self._show_config_graphics)
        config_thread.start()

    def _write_to_recently_opened(self, path_config_file):
        parent = os.path.dirname(self._determine_script_path())  # from /powermolegui/lib/ to /powermolegui/
        path_file_recent = os.path.join(parent, 'settings', 'recently_opened_config_file')
        with open(path_file_recent, 'w') as file:
            file.write(path_config_file)

    def _config_file_dialog(self):  # fix this py_lint error --> inconsistent-return-statements
        if self.is_busy:
            return None
        self.main_frame.canvas_frame.canvas_landscape.delete("all")
        file_types = [('powermole config file', '*.json')]
        self.path_config_file = askopenfilename(filetypes=file_types)
        if self.path_config_file:
            config_thread = threading.Thread(target=self._show_config_graphics)
            config_thread.start()
            self._write_to_recently_opened(self.path_config_file)

    def _get_configuration_file(self):
        """Retrieves the path instance var, parses the config file, and returns config object.

        This method is called by <show_config_graphics>, because in
        order to create and show the canvas items, it needs
        information about the real world hosts.
        """
        if not self.path_config_file:
            return None
        configuration = parse_configuration_file(self.path_config_file)  # import function
        if not configuration:
            self.path_config_file = None
            return None
        return configuration

    def _show_config_graphics(self):  # fix pylint inconsistent-return-statements
        """Creates canvas items and shows the landscape based on the config object.

        This method is called by _config_file_dialog when
        the user opens ("Open") a powermole configuration file.
        """
        self.configuration = self._get_configuration_file()
        if not self.configuration:
            return None
        items_generator = ItemsGenerator(self, self.configuration)
        self.canvas_items = items_generator.create_canvas_items()  # creates (and by default show) all canvas items
        items_generator.show_landscape(self.canvas_items)
        self.set_scrollregion()

    def run_powermole(self):  # fix this py_lint error --> inconsistent-return-statements
        """_________________."""
        if self.is_busy:
            return None
        run_thread = threading.Thread(target=application, args=(self,))
        run_thread.start()

    def stop_powermole(self):
        """Sets the should_terminate var to True.

        When the program, or rather, the business logic, is in
        FOR or TOR mode, it will run indefinitely. When the user
        hits ctrl + c, the window widget will capture the event,
        and sets the should_terminate to True. The business
        logic, polling this var, will break the loop, and
        dismantles the tunnel.

        Note: in COMMAND mode, the KeyboardInterrupt is passed
        from the widget to the logic, so no need for a
        polling mechanism.

        Note: in FILE mode, no need for KeyboardInterrupts.
        Once the files are transferred, the tunnel will be
        automatically dismantled.
        """
        self.should_terminate_powermole = True

    def close_window(self):
        """Closes the window when the business logic says so."""
        if not self.is_busy:
            self.should_terminate_powermole = True
            self.destroy()
        else:
            self._logger.info('*** window _cannot_ be closed during setup and operation of tunnel ***')


class TransferWindow(tk.Toplevel):
    """Represents an interface for the user to select files locally to be copied to destination host.

    IN DEVELOPMENT!

    """

    def __init__(self, *args, **kwargs):
        """Initialize the TopLevel object."""
        super().__init__(*args, **kwargs)  # with super(), no self as argument is needed
        self.scale = 0
        self.title("Interface")
        self._set_size()

    def _set_size(self):
        screen_width = self.winfo_screenwidth()  # width of the computer screen
        screen_height = self.winfo_screenheight()  # height of the computer screen
        self.scale = determine_scale(screen_width)
        win_width = WINDOW_WIDTH * self.scale  # width of the main window
        win_height = WINDOW_HEIGHT * self.scale  # height of the main window
        start_x = (screen_width / 2) - (win_width / 2)
        start_y = (screen_height / 2) - (win_height / 2)
        self.geometry('%dx%d+%d+%d' % (win_width, win_height, start_x, start_y))  # geometry behaves erratic!
        self.resizable(True, True)


class CommandWindow(tk.Toplevel):
    """Represents an interface for the user to issue commands and receive result."""

    def __init__(self, *args, **kwargs):
        """Initialize the TopLevel object."""
        super().__init__(*args, **kwargs)  # with super(), no self as argument is needed
        self.scale = 0
        self.title("Interface")
        self._bind_to_event()
        self._is_return_pressed = False
        self._terminate = False
        self.protocol("WM_DELETE_WINDOW", self._terminate_window)
        self.sub_command_window = CommandFrame(self)
        self._set_size()

    def _bind_to_event(self):
        self.bind("<Return>", lambda e: self._return_pressed())
        self.bind('<Control-c>', lambda e: self._terminate_window())

    def _set_size(self):
        screen_width = self.winfo_screenwidth()  # width of the computer screen
        screen_height = self.winfo_screenheight()  # height of the computer screen
        self.scale = determine_scale(screen_width)
        win_width = WINDOW_WIDTH * self.scale  # width of the main window
        win_height = WINDOW_HEIGHT * self.scale  # height of the main window
        start_x = (screen_width / 2) - (win_width / 2)
        start_y = (screen_height / 2) - (win_height / 2)
        self.geometry('%dx%d+%d+%d' % (win_width, win_height, start_x, start_y))  # geometry behaves erratic!
        self.resizable(True, True)

    def _return_pressed(self):
        self._is_return_pressed = True

    def _terminate_window(self):
        self._terminate = True

    def get_input(self):
        """Captures the input of the user and returns it."""
        while not self._is_return_pressed:  # when user hits the Enter key, capture the input
            if self._terminate:  # when user hits control + c, abort and close TopLevel (Command) window
                self.destroy()
                raise KeyboardInterrupt
            sleep(0.1)
        text = self.sub_command_window.command_entry.entry.get()
        self.sub_command_window.command_entry.entry.delete(0, 'end')
        self._is_return_pressed = False
        return text

    def show_response(self, line):
        """Shows the output sent by the Agent."""
        # text.insert(1.0) refers to line 1 (start) character 0
        self.sub_command_window.command_response.text.insert('end', line + '\n')
        self.sub_command_window.command_response.text.see("end")
