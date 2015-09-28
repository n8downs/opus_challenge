from urllib.parse import urljoin

class SiteCrawler:
    __USER_AGENT = 'SiteCrawler'

    def __init__(self, svc, domain):
        self.__svc = svc
        self.__domain = domain
        self.__urlsToFetch = []

        self.__robotParser = self.__svc.get('RobotFileParser')(urljoin(self.__domain, 'robots.txt'))
        self.__robotParser.read()

    def __parseContents(self, url):
        parsed = {"assets": [], "links": []}

    def map(self):
        siteMap = {}

        self.__urlsToFetch.append(self.__domain)

        while self.__urlsToFetch:
            url = self.__urlsToFetch.pop()

            if url in siteMap.keys():
                continue

            if not self.__robotParser.can_fetch(self.__USER_AGENT, url):
                siteMap[url] = "Disallowed by robots.txt"
                continue

            siteMap[url] = self.__parseContents(url)

        return siteMap
