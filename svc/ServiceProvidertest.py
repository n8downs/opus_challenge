import unittest
from .ServiceProvider import ServiceProvider

class BasicTests(unittest.TestCase):
    def setUp(self):
        self.serviceProvider = ServiceProvider()

    def test_register_and_get_a_service(self):
        obj = {}
        self.serviceProvider.register('obj', obj)
        self.assertIs(obj, self.serviceProvider.get('obj'))
        self.assertIsNot({}, self.serviceProvider.get('obj'))

    def test_trying_to_get_an_unregistered_service_throws(self):
        with self.assertRaises(Exception) as cm:
            self.serviceProvider.get('aoeu')

        self.assertEqual(("No service for 'aoeu' registered",), cm.exception.args)
