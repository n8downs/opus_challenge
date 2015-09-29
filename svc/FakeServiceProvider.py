from .ServiceProvider import ServiceProvider

class FakeRobotFileParser:
    def __init__(self, url):
        self._url = url

    def read(self):
        pass

    def can_fetch(self, agent, url):
        return True

class FakeResponse:
    def __init__(self, args):
        self.text = args.get('text', '');
        self.status_code = args.get('status_code', 200);

class FakeRequests:
    def __init__(self):
        self._calls = []
        self._expectations = {}

    def _expect(self, url, code, text):
        self._expectations[url] = FakeResponse({"status_code": code, "text": text})

    def get(self, url, headers={}):
        self._calls.append({"url": url, "headers": headers})

        response = self._expectations.get(url, False)
        if not response:
            raise Exception("No request expectation set for: '%s'" % (url,))

        return response

class FakeServiceProvider(ServiceProvider):
    def __init__(self):
        super().__init__()
        self.register('RobotFileParser', FakeRobotFileParser)
        self.register('requests', FakeRequests())
