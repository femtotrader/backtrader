#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
#
# Copyright (C) 2015, 2016 Daniel Rodriguez
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from .. import Observer


class DrawDown(Observer):
    '''This observer keeps track of the current drawdown level (plotted) and
    the maxdrawdown (not plotted) levels

    Params: None
    '''
    lines = ('drawdown', 'maxdrawdown',)

    plotinfo = dict(plot=True, subplot=True)

    plotlines = dict(maxdrawdown=dict(_plotskip='True',))

    def __init__(self):
        super(DrawDown, self).__init__()

        self.maxdd = 0.0
        self.peak = float('-inf')

    def next(self):
        value = self._owner.broker.getvalue()

        # update the maximum seen peak
        if value > self.peak:
            self.peak = value

        # calculate the current drawdown
        self.lines.drawdown[0] = dd = 100.0 * (self.peak - value) / self.peak

        # update the maxdrawdown if needed
        self.lines.maxdrawdown[0] = self.maxdd = max(self.maxdd, dd)
