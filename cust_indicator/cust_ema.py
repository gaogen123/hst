#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
#
# Copyright (C) 2015-2023 Daniel Rodriguez
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
from backtrader.indicators import MovingAverageBase, ExponentialSmoothing, ExponentialMovingAverage


class cust_ema(MovingAverageBase):
    '''
    A Moving Average that smoothes data exponentially over time.

    It is a subclass of SmoothingMovingAverage.

      - self.smfactor -> 2 / (1 + period)
      - self.smfactor1 -> `1 - self.smfactor`

    Formula:
      - movav = prev * (1.0 - smoothfactor) + newdata * smoothfactor

    See also:
      - http://en.wikipedia.org/wiki/Moving_average#Exponential_moving_average
    '''
    lines = ('cust_ema',)
    params = (
        ('n', 3),
        ('m', 1),
    )

    def __init__(self):
        # Before super to ensure mixins (right-hand side in subclassing)
        # can see the assignment operation and operate on the line
        self.lines[0] = es = ExponentialSmoothing(
            self.data,
            period=self.p.period,
            alpha=self.p.m/self.p.n)

        self.alpha, self.alpha1 = es.alpha, es.alpha1

        super(cust_ema, self).__init__()
