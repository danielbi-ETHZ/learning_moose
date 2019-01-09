#!/usr/bin/env python2
#* This file is part of the MOOSE framework
#* https://www.mooseframework.org
#*
#* All rights reserved, see COPYRIGHT for full restrictions
#* https://github.com/idaholab/moose/blob/master/COPYRIGHT
#*
#* Licensed under LGPL 2.1, please see LICENSE for details
#* https://www.gnu.org/licenses/lgpl-2.1.html

import unittest

from MooseDocs.tree import html

class TestHTML(unittest.TestCase):
    """
    Tests for html tree structure.
    """
    def testTag(self):
        tag = html.Tag(None, 'section')
        self.assertEqual(tag.write(), '<section></section>')

    def testString(self):
        tag = html.String(content=u'section')
        self.assertEqual(tag.write(), 'section')

        tag = html.String(content=u'<section>', escape=True)
        self.assertEqual(tag.write(), '&lt;section&gt;')

    def testTagString(self):
        tag = html.Tag(None, 'h1')
        html.String(content=u'foo', parent=tag)
        self.assertEqual(tag.write(), '<h1>foo</h1>')

if __name__ == '__main__':
    unittest.main(verbosity=2)
