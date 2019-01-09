#pylint: disable=missing-docstring
#* This file is part of the MOOSE framework
#* https://www.mooseframework.org
#*
#* All rights reserved, see COPYRIGHT for full restrictions
#* https://github.com/idaholab/moose/blob/master/COPYRIGHT
#*
#* Licensed under LGPL 2.1, please see LICENSE for details
#* https://www.gnu.org/licenses/lgpl-2.1.html

from MooseDocs.extensions import core, command

def make_extension(**kwargs):
    return CommonExtension(**kwargs)

class CommonExtension(command.CommandExtension):
    """
    Allows common shortcuts to be defined within the configure file.
    """

    @staticmethod
    def defaultConfig():
        config = command.CommandExtension.defaultConfig()
        config['shortcuts'] = (dict(), "Key-value pairs to insert as shortcuts, this should be " \
                                       "a dictionary or a dictionary of dictionaries.")
        return config

    def extend(self, reader, renderer):
        self.requires(core)

    def postTokenize(self, ast, page, meta, reader): #pylint: disable=unused-argument
        if ast.is_root:
            shortcuts = self.get('shortcuts', dict())
            for key, value in shortcuts.iteritems():
                if isinstance(value, dict):
                    for k, v in value.iteritems():
                        core.Shortcut(ast, key=unicode(k), link=unicode(v), string=unicode(k))
                else:
                    core.Shortcut(ast, key=unicode(key), link=unicode(value), string=unicode(key))
