import sys
from crawler import Crawler
from svc.RealServiceProvider import RealServiceProvider

def main():
    domain = sys.argv[1]
    svc = RealServiceProvider()
    crawler = Crawler(svc, domain)
    print("Mapping...")
    siteMap = crawler.map(verbose=True)
    print("Complete.")
    print()
    print("SiteMap:")
    for url, data in siteMap.items():
        print(url)

        for prop in ['error', 'original_url', 'redirects_to']:
            if data.get(prop, False):
                print('  %s: %s' % (prop, data[prop],))

        for prop in ['assets', 'links']:
            print('  %s:' % (prop,))
            for p in data.get(prop, []):
                print('    %s' % (p,))

if __name__ == "__main__":
    main()
