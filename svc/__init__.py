from urllib.robotparser import RobotFileParser


class ServiceProvider:
    def __init__(self):
        self.__services = {};

    def get(self, name):
        if not name in self.__services.keys():
            raise Exception("No service for '%s' registered" % (name,))

        return self.__services[name]

    def register(self, name, service):
        self.__services[name] = service;


class RealServiceProvider(ServiceProvider):
    def __init__(self):
        super().__init__()
        self.register('RobotFileParser', RobotFileParser)

class FakeServiceProvider(ServiceProvider):
    def __init__(self):
        super().__init__()
        self.register('RobotParser', {}) # TODO: Fake
