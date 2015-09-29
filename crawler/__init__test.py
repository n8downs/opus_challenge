import unittest
from svc.FakeServiceProvider import FakeServiceProvider
from crawler import Crawler

class BasicTests(unittest.TestCase):
    def setUp(self):
        self.svc = FakeServiceProvider()

    def test_links_are_captured(self):
        self.svc.get('requests')._expect("http://example.com", 200, '<a href="http://example.com/foobar/">click here</a>')

        crawler = Crawler(self.svc, "http://example.com")
        siteMap = crawler.map()
        self.assertEqual({"http://example.com":{"assets":[], "links":["http://example.com/foobar/"]}}, siteMap)

if __name__ == '__main__':
    unittest.main()
