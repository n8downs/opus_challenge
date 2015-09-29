import unittest
from svc.FakeServiceProvider import FakeServiceProvider
from crawler import Crawler

class LinkTests(unittest.TestCase):
    def setUp(self):
        self.svc = FakeServiceProvider()

    def tearDown(self):
        self.assertEqual(0, self.svc.get('requests')._countExpectations())

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

    def test_leaving_out_scheme_in_domain_is_fine(self):
        self.svc.get('requests')._expect("http://example.com", 200, '<a href="http://example.com">click here</a>')

        crawler = Crawler(self.svc, "example.com")
        siteMap = crawler.map()
        self.assertEqual({"http://example.com":{"assets":[], "links":["http://example.com"]}}, siteMap)

    def test_https_counts_as_internal_link(self):
        self.svc.get('requests')._expect("http://example.com", 200, '<a href="https://example.com/secure">click here</a>')
        self.svc.get('requests')._expect("https://example.com/secure", 200, '<different><stuff>')

        crawler = Crawler(self.svc, "http://example.com")
        siteMap = crawler.map()
        self.assertEqual({"http://example.com":{"assets":[], "links":["https://example.com/secure"]},
                          "https://example.com/secure": {"assets": [], "links": []}}, siteMap)

    def test_http_counts_as_internal_link(self):
        self.svc.get('requests')._expect("https://example.com", 200, '<a href="http://example.com/insecure">click here</a>')
        self.svc.get('requests')._expect("http://example.com/insecure", 200, '<different><stuff>')

        crawler = Crawler(self.svc, "https://example.com")
        siteMap = crawler.map()
        self.assertEqual({"https://example.com":{"assets":[], "links":["http://example.com/insecure"]},
                          "http://example.com/insecure": {"assets": [], "links": []}}, siteMap)

    def test_subdomain_doesnt_count_as_internal(self):
        self.svc.get('requests')._expect("http://example.com", 200, '<a href="http://api.example.com">click here</a>')

        crawler = Crawler(self.svc, "http://example.com")
        siteMap = crawler.map()
        self.assertEqual({"http://example.com":{"assets":[], "links":["http://api.example.com"]}}, siteMap)

    # this may not be expected behavior, but I wanted to leave the characterization test
    def test_www_subdomain_doesnt_count_as_internal(self):
        self.svc.get('requests')._expect("http://example.com", 200, '<a href="http://www.example.com">click here</a>')

        crawler = Crawler(self.svc, "http://example.com")
        siteMap = crawler.map()
        self.assertEqual({"http://example.com":{"assets":[], "links":["http://www.example.com"]}}, siteMap)

    def test_redirects_are_handled_nicely(self):
        self.svc.get('requests')._expect(
            "http://example.com",
            200,
            '<a href="https://www.example.com/foobar">click here</a>',
            finalUrl="https://www.example.com")
        self.svc.get('requests')._expect("https://www.example.com/foobar", 200, '')

        crawler = Crawler(self.svc, "example.com")
        siteMap = crawler.map()
        self.assertEqual({"https://www.example.com":{"original_url": "http://example.com", "assets":[], "links":["https://www.example.com/foobar"]},
                          "https://www.example.com/foobar": {"assets": [], "links": []}}, siteMap)

    def test_disallowed_urls_are_not_fetched(self):
        self.svc.get('requests')._expect("http://example.com", 200, '<a href="http://example.com/admin">click here</a>')
        self.svc.get('RobotFileParser')._disallowed_urls['http://example.com/admin'] = True

        crawler = Crawler(self.svc, "http://example.com")
        siteMap = crawler.map()
        self.assertEqual({"http://example.com":{"assets":[], "links":["http://example.com/admin"]},
                         "http://example.com/admin": {"error": "Disallowed by robots.txt"}}, siteMap)

    def test_error_urls_are_noted(self):
        self.svc.get('requests')._expect("http://example.com", 400, 'Error: bad request')

        crawler = Crawler(self.svc, "http://example.com")
        siteMap = crawler.map()
        self.assertEqual({"http://example.com":{"error": "Error fetching url. Response code: 400"}}, siteMap)

class AssetTests(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
