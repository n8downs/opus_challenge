from .ServiceProvider import ServiceProvider
from urllib.robotparser import RobotFileParser
import requests

class RealServiceProvider(ServiceProvider):
    def __init__(self):
        super().__init__()
        self.register('RobotFileParser', RobotFileParser)
        self.register('requests', requests)
