import unittest


class TestApp(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_app(self):
        from pymapplot import number
        self.assertEqual(number, 3)