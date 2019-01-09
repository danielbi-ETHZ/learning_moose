#pylint: disable=missing-docstring,no-member
#* This file is part of the MOOSE framework
#* https://www.mooseframework.org
#*
#* All rights reserved, see COPYRIGHT for full restrictions
#* https://github.com/idaholab/moose/blob/master/COPYRIGHT
#*
#* Licensed under LGPL 2.1, please see LICENSE for details
#* https://www.gnu.org/licenses/lgpl-2.1.html
#pylint: enable=missing-docstring
import re
from base import NodeBase
from MooseDocs.common import exceptions

def escape(text):
    """
    Escape LaTeX commands.

    Inputs:
        text: a plain text message
    """
    conv = {
        '&': '\\&',
        '%': '\\%',
        '$': '\\$',
        '#': '\\#',
        '_': '\\_',
        '{': '\\{',
        '}': '\\}',
        '^': '{\\textasciicircum}',
        '~': '{\\textasciitilde}',
        '\\': '{\\textbackslash}',
        '<': '{\\textless}',
        '>': '{\\textgreater}',
    }

    regex_list = []
    for key in sorted(conv.keys(), key=lambda item: - len(item)): #pylint: disable=consider-iterating-dictionary
        regex_list.append(re.escape(unicode(key)))
    regex = re.compile('|'.join(regex_list))
    return regex.sub(lambda match: conv[match.group()], text)

class LatexBase(NodeBase):
    """Base class for Latex nodes."""
    def __init__(self, *args, **kwargs):
        string = kwargs.pop('string', None)
        NodeBase.__init__(self, *args, **kwargs)

        if string is not None:
            String(self, content=string)

class EnclosureBase(LatexBase):
    """
    Class for enclosing other nodes in characters, e.g. [], {}.
    """
    def __init__(self, *args, **kwargs):
        LatexBase.__init__(self, *args, **kwargs)

        if self.get('enclose', None) is None:
            raise exceptions.MooseDocsException("The 'enclose' property is required.")

    def write(self):
        """
        Write LaTeX as a string.
        """
        enclose = self.get('enclose')
        out = enclose[0]
        for child in self.children:
            out += child.write()
        out += enclose[1]
        return out

class Bracket(EnclosureBase):
    """
    Square bracket enclosure ([]).
    """
    def __init__(self, parent=None, **kwargs):
        EnclosureBase.__init__(self, 'Bracket', parent, enclose=('[', ']'), **kwargs)

class Brace(EnclosureBase):
    """
    Curly brace enclosure ({}).
    """
    def __init__(self, parent=None, **kwargs):
        EnclosureBase.__init__(self, 'Brace', parent, enclose=('{', '}'), **kwargs)

class InlineMath(EnclosureBase):
    """
    Math enclosure ($$).
    """
    def __init__(self, parent=None, **kwargs):
        EnclosureBase.__init__(self, 'InlineMath', parent, enclose=('$', '$'), **kwargs)

class Command(LatexBase):
    """
    Typical zero or one argument command: \foo{bar}.

    If children do not exist then the braces are not included (e.g., \foo).
    """
    def __init__(self, parent, name, **kwargs):
        kwargs.setdefault('start', u'')
        kwargs.setdefault('end', u'')
        kwargs.setdefault('options', dict())
        LatexBase.__init__(self, name, parent, **kwargs)

    def write(self):
        out = self.get('start')
        out += '\\%s' % self.name
        if self.children:
            out += '{'
            for child in self.children:
                out += child.write()
            out += '}'
        out += self.get('end')
        return out

class CustomCommand(LatexBase):
    """
    Class for building up arbitrary commands.

    Children should be Bracket or Brace objects to build up the command.
    """
    def __init__(self, parent, name, **kwargs):
        kwargs.setdefault('start', u'')
        kwargs.setdefault('end', u'')
        LatexBase.__init__(self, name, parent, **kwargs)

    def write(self):
        """
        Write to LaTeX string.
        """
        out = self.get('start')
        out += '\\%s' % self.name
        for child in self.children:
            out += child.write()
        out += self.get('end')
        return out

class Environment(LatexBase):
    """
    Class for LaTeX environment: \\begin{foo}...\\end{foo}
    """
    def __init__(self, parent, name, **kwargs):
        kwargs.setdefault('start', u'\n')
        kwargs.setdefault('end', u'')
        kwargs.setdefault('after_begin', u'\n')
        kwargs.setdefault('before_end', u'\n')
        LatexBase.__init__(self, name, parent, **kwargs)

    def write(self):
        """
        Write to LaTeX string.
        """
        out = '%s\\begin{%s}%s' % (self.get('start'), self.name, self.get('after_begin'))
        for child in self.children:
            out += child.write()
        out += '%s\\end{%s}%s' % (self.get('before_end'), self.name, self.get('end'))
        return out

class String(NodeBase):
    """
    A node for containing string content, the parent must always be a Tag.
    """
    def __init__(self, parent=None, **kwargs):
        kwargs.setdefault('content', u'')
        kwargs.setdefault('escape', True)
        NodeBase.__init__(self, 'String', parent, **kwargs)

    def write(self):
        """
        Write to LaTeX string.
        """
        out = escape(self.get('content')) if self.get('escape') else self.get('content')
        for child in self.children:
            out += child.write()
        return out
