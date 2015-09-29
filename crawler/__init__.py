from urllib.parse import urljoin, urldefrag, urlparse
from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.assets = []
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            link = False
            for attr in attrs:
                name, value = attr
                if name == 'href':
                    link = value
            if (link):
                self.links.append(link)


class Crawler:
    __USER_AGENT = 'SiteCrawlerBot/0.1'

    def __init__(self, svc, domain):
        self.__svc = svc
        self.__domain = domain
        self.__urlsToFetch = []

        self.__robotParser = self.__svc.get('RobotFileParser')(urljoin(self.__domain, 'robots.txt'))
        self.__robotParser.read()

    def __parseContents(self, url):
        response = self.__svc.get('requests').get(url, headers={"User-Agent": self.__USER_AGENT, "Accept": "text/html"})
        if response.status_code >= 400:
            pass
            #return "Error: %d" % (response.status_code,)

        print(response.status_code)
        print(response.text)

        parser = MyHTMLParser()
        parser.feed(response.text)

        for link in parser.links:
            url, fragment = urldefrag(urljoin(url, link))
            self.__urlsToFetch.append(url)

        return {"assets": parser.assets, "links": parser.links}

    def map(self):
        siteMap = {}

        parsedDomain = urlparse(self.__domain)
        self.__urlsToFetch.append(self.__domain)

        while self.__urlsToFetch:
            url = self.__urlsToFetch.pop()

            if url in siteMap.keys():
                continue

            parsedUrl = urlparse(url)
            if parsedUrl.scheme not in ['http', 'https']:
                continue

            if parsedDomain.netloc != parsedUrl.netloc:
                continue

            if not self.__robotParser.can_fetch(self.__USER_AGENT, url):
                siteMap[url] = "Disallowed by robots.txt"
                continue

            siteMap[url] = self.__parseContents(url)

        return siteMap
