import unittest
from svc.FakeServiceProvider import FakeServiceProvider
from crawler import Crawler

class BasicTests(unittest.TestCase):
    def setUp(self):
        self.svc = FakeServiceProvider()

    def test_absolute_links_are_captured(self):
        self.svc.get('requests')._expect("http://example.com", 200, '<a href="http://example.com/foobar/">click here</a>')
        self.svc.get('requests')._expect("http://example.com/foobar/", 200, '')

        crawler = Crawler(self.svc, "http://example.com")
        siteMap = crawler.map()
        self.assertEqual({"http://example.com":{"assets":[], "links":["http://example.com/foobar/"]},
                          "http://example.com/foobar/": {"assets": [], "links": []}}, siteMap)

    def test_relative_links_are_captured(self):
        self.svc.get('requests')._expect("http://example.com", 200, '<a href="foobar/">click here</a>')
        self.svc.get('requests')._expect("http://example.com/foobar/", 200, '')

        crawler = Crawler(self.svc, "http://example.com")
        siteMap = crawler.map()
        self.assertEqual({"http://example.com":{"assets":[], "links":["foobar/"]},
                          "http://example.com/foobar/": {"assets": [], "links": []}}, siteMap)

    def test_hash_links_are_not_captured(self):
        self.svc.get('requests')._expect("http://example.com", 200, '<a href="#foobar">click here</a>')

        crawler = Crawler(self.svc, "http://example.com")
        siteMap = crawler.map()
        self.assertEqual({"http://example.com":{"assets":[], "links":["#foobar"]}}, siteMap)

    def test_query_params_are_captured(self):
        self.svc.get('requests')._expect("http://example.com", 200, '<a href="/?foo=bar">click here</a>')
        self.svc.get('requests')._expect("http://example.com/?foo=bar", 200, '<different><stuff>')

        crawler = Crawler(self.svc, "http://example.com")
        siteMap = crawler.map()
        self.assertEqual({"http://example.com":{"assets":[], "links":["/?foo=bar"]},
                          "http://example.com/?foo=bar": {"assets": [], "links": []}}, siteMap)

    def test_mailto_links_are_not_captured(self):
        self.svc.get('requests')._expect("http://example.com", 200, '<a href="mailto:foo@bar.com">click here</a>')

        crawler = Crawler(self.svc, "http://example.com")
        siteMap = crawler.map()
        self.assertEqual({"http://example.com":{"assets":[], "links":["mailto:foo@bar.com"]}}, siteMap)

    def test_external_links_are_not_captured(self):
        self.svc.get('requests')._expect("http://example.com", 200, '<a href="http://foobar.com">click here</a>')

        crawler = Crawler(self.svc, "http://example.com")
        siteMap = crawler.map()
        self.assertEqual({"http://example.com":{"assets":[], "links":["http://foobar.com"]}}, siteMap)

    def test_recursive_links_dont_cause_re_fetch(self):
        self.svc.get('requests')._expect("http://example.com", 200, '<a href="http://example.com">click here</a>')

        crawler = Crawler(self.svc, "http://example.com")
        siteMap = crawler.map()
        self.assertEqual({"http://example.com":{"assets":[], "links":["http://example.com"]}}, siteMap)

    # def test_leaving_out_scheme_in_domain_is_fine(self):
    # def test_https_counts_as_internal_link(self):
    # def test_http_counts_as_internal_link(self):
    # def test_subdomain_doesnt_count_as_internal(self):

if __name__ == '__main__':
    unittest.main()
