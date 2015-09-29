from urllib.parse import urlparse
from .ServiceProvider import ServiceProvider
import requests

class FakeRobotFileParser:
    _disallowed_urls = {}

    def __init__(self, url):
        self._url = url

    def read(self):
        pass

    def can_fetch(self, agent, url):
        return not FakeRobotFileParser._disallowed_urls.get(url, False)

class FakeResponse:
    def __init__(self, args):
        self.text = args.get('text', '');
        self.status_code = args.get('status_code', 200);
        self.url = args.get('finalUrl', None) or args["url"]

class FakeExceptionsModule:
    def __init__(self):
        class RequestException(IOError):
            pass

        class InvalidSchema(RequestException):
            pass

        self.RequestException = RequestException
        self.InvalidSchema = InvalidSchema

class FakeRequests:
    def __init__(self):
        self._calls = []
        self._expectations = {}

        self.exceptions = FakeExceptionsModule()

    def _expect(self, url, code, text, finalUrl=None):
        self._expectations[url] = FakeResponse({
            "status_code": code,
            "text": text,
            "url": url,
            "finalUrl": finalUrl})

    def get(self, url, headers={}):
        self._calls.append({"url": url, "headers": headers})

        response = self._expectations.get(url, False)
        if not response:
            raise Exception("No request expectation set for: '%s'" % (url,))

        del self._expectations[url]

        if urlparse(response.url).scheme not in ['http', 'https']:
            raise self.exceptions.InvalidSchema("Unrecognized scheme: %s" % (response.url))

        return response

    def _countExpectations(self):
        return len(self._expectations)

class FakeServiceProvider(ServiceProvider):
    def __init__(self):
        super().__init__()
        self.register('RobotFileParser', FakeRobotFileParser)
        self.register('requests', FakeRequests())
