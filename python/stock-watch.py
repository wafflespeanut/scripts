from datetime import datetime
from threading import Thread
from time import sleep

import sys, urllib2

args = sys.argv[1:]
name = args[0] if args else 'ashley'
interval_secs = float(args[1]) if len(args) > 1 else 1

url_1 = 'http://getquote.icicidirect.com/trading_stock_quote.aspx?Symbol=%s' % name
url_2 = 'https://secure.icicidirect.com/IDirectTrading/trading/trading_stock_bestbid.aspx?Symbol=%s' % name

last_share = 0
filename = name + datetime.now().strftime('-%Y-%m-%d')

# Thread that returns value on joining (https://stackoverflow.com/a/6894023/2313792)
class ReturningThread(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs, Verbose)
        self._return = None

    def run(self):
        if self._Thread__target is not None:
            self._return = self._Thread__target(*self._Thread__args, **self._Thread__kwargs)

    def join(self):
        Thread.join(self)
        return self._return

while True:
    try:
        thread = ReturningThread(target=lambda: urllib2.urlopen(url_2).read())
        thread.start()
        body_1 = urllib2.urlopen(url_1).read()
        body_2 = thread.join()
    except urllib2.URLError:
        continue
    l1 = map(lambda t: t.strip(), body_1.split('\n'))
    l2 = map(lambda t: t.strip(), body_2.split('\n'))
    offset = 3

    def g(key):
        idx = l1.index(key)
        return l1[idx + offset]

    last_price = float(g('LAST TRADE PRICE'))
    day_volume = int(''.join(g('DAY VOLUME').split(',')))
    day_high, day_low = float(g('DAY HIGH')), float(g('DAY LOW'))

    if last_share:
        line = '[%s]: %s\t%s\t%s\t%s\t(%s, %s)' % \
               (g('DATE'), g('LAST TRADED TIME'), last_price, day_volume - last_share, day_volume, day_low, day_high)
        print line

        idx = 116
        for _ in range(5):      # 5 rows
            end = idx + 7 * offset      # 7 cols
            print '\t'.join(map(lambda i: l2[i], range(idx, end + 1, offset))[:4])
            idx = end + 5

        with open(filename, 'a') as fd:
            fd.write(line + '\n')
    last_share = day_volume
    sleep(interval_secs)
