from unittest import TestCase
import test_helper as th

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
