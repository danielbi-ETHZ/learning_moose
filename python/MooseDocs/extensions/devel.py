#pylint: disable=missing-docstring
#* This file is part of the MOOSE framework
#* https://www.mooseframework.org
#*
#* All rights reserved, see COPYRIGHT for full restrictions
#* https://github.com/idaholab/moose/blob/master/COPYRIGHT
#*
#* Licensed under LGPL 2.1, please see LICENSE for details
#* https://www.gnu.org/licenses/lgpl-2.1.html

import importlib
from MooseDocs.common import exceptions
from MooseDocs.extensions import core, floats, command, table

def make_extension(**kwargs):
    return DevelExtension(**kwargs)

class DevelExtension(command.CommandExtension):
    """
    Adds features useful for MooseDocs developers such as example blocks and settings tables.
    """
    @staticmethod
    def defaultConfig():
        config = command.CommandExtension.defaultConfig()
        config['test'] = (None, "A configuration item for testing purposes, it does nothing.")
        return config

    def extend(self, reader, renderer):
        self.requires(core, floats)
        self.addCommand(reader, Example())
        self.addCommand(reader, ComponentSettings())

class Example(command.CommandComponent):
    COMMAND = 'devel'
    SUBCOMMAND = 'example'

    @staticmethod
    def defaultSettings():
        settings = command.CommandComponent.defaultSettings()
        settings.update(floats.caption_settings())
        settings['prefix'] = (u'Example', settings['prefix'][1])
        return settings

    def createToken(self, parent, info, page):
        master = floats.create_float(parent, self.extension, self.reader, page,
                                     self.settings, **self.attributes)
        data = info['block'] if 'block' in info else info['inline']
        core.Code(master, content=data)
        return master

class ComponentSettings(command.CommandComponent):
    COMMAND = 'devel'
    SUBCOMMAND = 'settings'

    @staticmethod
    def defaultSettings():
        settings = command.CommandComponent.defaultSettings()
        settings['module'] = (None, "The name of the module containing the object.")
        settings['object'] = (None, "The name of the object to import from the 'module'.")
        settings.update(floats.caption_settings())
        settings['prefix'] = (u'Table', settings['prefix'][1])

        return settings

    def createToken(self, parent, info, page):
        if self.settings['module'] is None:
            raise exceptions.MooseDocsException("The 'module' setting is required.")

        if self.settings['object'] is None:
            raise exceptions.MooseDocsException("The 'object' setting is required.")

        master = floats.create_float(parent, self.extension, self.reader, page, self.settings,
                                     **self.attributes)
        try:
            mod = importlib.import_module(self.settings['module'])
        except ImportError:
            msg = "Unable to load the '{}' module."
            raise exceptions.MooseDocsException(msg, self.settings['module'])

        try:
            obj = getattr(mod, self.settings['object'])
        except AttributeError:
            msg = "Unable to load the '{}' attribute from the '{}' module."
            raise exceptions.MooseDocsException(msg, self.settings['object'],
                                                self.settings['module'])

        if hasattr(obj, 'defaultSettings'):
            settings = obj.defaultSettings()
        elif hasattr(obj, 'defaultConfig'):
            settings = obj.defaultConfig()
        else:
            msg = "The '{}' object in the '{}' module does not have a 'defaultSettings' or "\
                  "'defaultConfig' method."
            raise exceptions.MooseDocsException(msg, mod, obj)

        rows = [[key, value[0], value[1]] for key, value in settings.iteritems()]
        tbl = table.builder(rows, headings=[u'Key', u'Default', u'Description'])
        tbl.parent = master
        return master
