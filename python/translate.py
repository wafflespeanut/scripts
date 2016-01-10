import sys, urllib2

DEFAULT = 'Hello, world!'
LOOKUP_NODE = 'class="t0"'
YELLOW, NULL = ('', '') if sys.platform == 'win32' else ('\033[93m', '\033[0m')

def translate(string, from_lang, to_lang):  # Makes use of Google translate for mobile
    url = 'https://translate.google.com/m?sl=%s&tl=%s&q=%s' % (from_lang, to_lang, string.replace(' ', '+'))
    fake_request = urllib2.Request(url, headers = {'User-Agent': 'Mozilla/5.0'})
    response = urllib2.urlopen(fake_request)
    page_source = response.read().decode('utf-8')
    node_idx = page_source.find(LOOKUP_NODE) + 1
    next_idx = page_source.find('<', node_idx)
    return page_source[(node_idx + len(LOOKUP_NODE)) : next_idx]

if __name__ == '__main__':
    _name, args = sys.argv[0], sys.argv[1:]
    word = args[0] if args else DEFAULT
    from_lang, to_lang = args[1].split('-') if (len(args) > 1 and '-' in args[1]) \
                                            else ('auto', args[1]) if len(args) > 1 \
                                                                 else ('en', 'fr')
    print YELLOW + word, '->', translate(word, from_lang, to_lang) + NULL
