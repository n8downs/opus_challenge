from urllib.parse import urljoin, urldefrag, urlparse
from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.assets = []
        self.links = []

    def handle_starttag(self, tag, attrs):
        def findAttr(name):
            found = False
            for n, v in attrs:
                if n == name:
                    found = v
            return found

        if tag == 'a':
            link = findAttr('href')
            if (link):
                self.links.append(link)
        else:
            for t, a in [('img', 'src'), ('script', 'src'), ('link', 'href')]:
                if t == tag:
                    asset = findAttr(a)
                    if asset:
                        self.assets.append(asset)

class Crawler:
    __USER_AGENT = 'SiteCrawlerBot/0.1'

    def __init__(self, svc, domain):
        self.__svc = svc

        self.__domain = domain if domain.startswith('http') else 'http://' + domain

        self.__urlsToFetch = []

        self.__robotParser = self.__svc.get('RobotFileParser')(urljoin(self.__domain, 'robots.txt'))
        self.__robotParser.read()

    def __parseContents(self, url):
        response = self.__svc.get('requests').get(url, headers={"User-Agent": self.__USER_AGENT, "Accept": "text/html"})
        if response.status_code >= 400:
            return {"error": "Error fetching url. Response code: %d" % (response.status_code,)}

        parser = MyHTMLParser()
        parser.feed(response.text)

        result = {"assets": parser.assets, "links": parser.links}
        if response.url != url:
            result["redirected_to"] = response.url

        return result

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
                siteMap[url] = {"error": "Disallowed by robots.txt"}
                continue

            contents = self.__parseContents(url)

            if contents.get("redirected_to", False):
                contents["original_url"] = url
                url = contents["redirected_to"]
                del contents["redirected_to"]

                if contents["original_url"] == self.__domain:
                    self.__domain = url
                    parsedDomain = urlparse(self.__domain)

                siteMap[contents["original_url"]] = {"redirects_to": url}

            siteMap[url] = contents

            for link in contents.get("links", []):
                url, fragment = urldefrag(urljoin(url, link))
                self.__urlsToFetch.append(url)


        return siteMap
