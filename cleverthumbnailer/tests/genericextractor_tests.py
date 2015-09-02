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

from unittest import TestCase, main

from cleverthumbnailer.featureextractor import GenericExtractor

class TestGenericExtractor(TestCase):
    def test_SR(self):
        self.assertRaises(TypeError, lambda _: GenericExtractor())
        self.assertRaises(TypeError, lambda _: GenericExtractor('string'))
        self.assertRaises(TypeError, lambda _: GenericExtractor(-1))
        self.assertRaises(TypeError, lambda _: GenericExtractor((2.1)))
        x = GenericExtractor(44100)
        self.assertEqual(x.sr, 44100)
        x.processRemaining()
        self.assertEqual(x.features, None) # should have no features

if __name__ == '__main__':
    main()
