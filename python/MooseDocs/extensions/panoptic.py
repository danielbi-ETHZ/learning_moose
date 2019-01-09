#pylint: disable=missing-docstring
#* This file is part of the MOOSE framework
#* https://www.mooseframework.org
#*
#* All rights reserved, see COPYRIGHT for full restrictions
#* https://github.com/idaholab/moose/blob/master/COPYRIGHT
#*
#* Licensed under LGPL 2.1, please see LICENSE for details
#* https://www.gnu.org/licenses/lgpl-2.1.html
import logging
from MooseDocs.extensions import common
LOG = logging.getLogger(__name__)
def make_extension(**kwargs):
    LOG.warning("The panoptic extension has been renamed, use MooseDocs.extensions.common.")
    return common.make_extension(**kwargs)
