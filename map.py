import sys
from crawler import Crawler
from svc.RealServiceProvider import RealServiceProvider

def main():
    domain = sys.argv[1]
    svc = RealServiceProvider()
    crawler = Crawler(svc, domain)
    print("Mapping %s" % (domain,))
    siteMap = crawler.map()
    for url, data in siteMap.items():
        print(url)
        if isinstance(data, str):
            print('  %s' % (data,))
            continue

        print('  assets:')
        for asset in data['assets']:
            print('    %s' % (asset,))
        print('  links:')
        for link in data['links']:
            print('    %s' % (link,))

if __name__ == "__main__":
    main()
