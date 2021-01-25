from unittest import TestCase
import test_helper as th
import math


class Test(TestCase):

    def test_format_postcode(self):
        p1 = th.format_postcode('B64 5QQ')
        self.assertEqual(p1, 'B64 5QQ')

        p2 = th.format_postcode('B645QQ')
        self.assertEqual(p2, 'B64 5QQ')

        p3 = th.format_postcode('B64DL')
        self.assertEqual(p3, 'B6 4DL')

        p4 = th.format_postcode('b64dL')
        self.assertEqual(p4, 'B6 4DL')

        p5 = th.format_postcode('SW90FA')
        self.assertEqual(p5, 'SW9 0FA')

        p6 = th.format_postcode('    SW90FA    ')
        self.assertEqual(p6, 'SW9 0FA')

        p7 = th.format_postcode('S W 9 0 F A')
        self.assertEqual(p7, 'SW9 0FA')




    def test_get_postcode_data(self):
        p1 = th.get_postcode_data('B64 5QQ')
        self.assertIsInstance(p1['county_name'], str)

        p2 = th.get_postcode_data('B645QQ')
        self.assertIsInstance(p2['county_name'], str)

        p3 = th.get_postcode_data('Not a postcode')
        self.assertIsNone(p3)

        p4 = th.get_postcode_data('')
        self.assertIsNone(p4)

        p5 = th.get_postcode_data('        ')
        self.assertIsNone(p5)
