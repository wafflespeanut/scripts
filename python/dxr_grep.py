import os, dryscrape
from lxml.html import HtmlElement, document_fromstring
from time import sleep

REPO = 'mozilla-central'
# sleeping is necessary for getting the entire page (JS stuff is loaded async)
SCRAPE_SLEEP_TIMEOUT = 2


def search_dxr(word, print_results=True):
    url = 'https://dxr.mozilla.org/%s/search?q=%s' % (REPO, word)
    print '\nScraping results from DXR: %s' % url
    session = dryscrape.Session()
    session.visit(url)
    print 'Sleeping for %s seconds...\n' % SCRAPE_SLEEP_TIMEOUT
    sleep(SCRAPE_SLEEP_TIMEOUT)
    response = session.body()

    files = {}
    found = 0
    doc = document_fromstring(response)
    results = doc.xpath('//div[@id="content"]/div[@class="results"]/div[@class="result"]')
    results_hint = doc.xpath('//div[@id="content"]/p[@class="top-of-tree"]')[0].text_content().strip()
    total_results = int(''.join(results_hint.split()[0].split(',')))

    for element in results:
        rel_path = element.get('data-path')
        lines = map(lambda e: int(e.get('data-line')), element.getchildren()[1:])
        code = map(HtmlElement.text_content, element.xpath('div[@class="result_line"]/div/a/code'))
        if print_results:
            for i, line in zip(lines, code):
                print '%s:%d: %s' % (rel_path, i, line)
        files.setdefault(rel_path, [])
        files[rel_path].extend(lines)
        found += len(lines)

    if found < total_results:
        print '\n\033[91mObtained only the top %d results from %d matches!\033[0m' % (found, total_results)

    return files, found == total_results
