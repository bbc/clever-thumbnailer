# Copyright (C) 2015 British Broadcasting Corporation
#
# Cleverthumbnailer is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# Cleverthumbnailer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Cleverthumbnailer; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.

from unittest import TestCase

from cleverthumbnailer.utils.mathtools import coerceThumbnail

__author__ = 'jont'

class TestCoerceThumbnail(TestCase):
    def test_values(self):
        self.assertEquals(coerceThumbnail(0, 20, 40), (0, 20))
        self.assertEquals(coerceThumbnail(0, 40, 40), (0, 40))
        self.assertEquals(coerceThumbnail(10, 20, 40), (10, 20))
        self.assertEquals(coerceThumbnail(10, 30, 25), (5, 25))
        self.assertEquals(coerceThumbnail(-10, 10, 25), (0, 20))

    def test_assert(self):
        with self.assertRaises(AssertionError):
            coerceThumbnail(0, 40, 20)

    pass
