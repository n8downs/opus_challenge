import sys
from sitecrawler import SiteCrawler
from svc import RealServiceProvider

def main():
    domain = sys.argv[1]
    svc = RealServiceProvider()
    crawler = SiteCrawler(svc, domain)
    print("Mapping %s" % (domain,))
    print(crawler.map())

if __name__ == "__main__":
    main()
