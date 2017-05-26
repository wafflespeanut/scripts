from datetime import datetime
from threading import Thread
from time import sleep

import fcntl, struct, sys, termios, tty, urllib2

class Watcher(object):
    def __init__(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        # reset with `termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)`
        tty.setraw(sys.stdin)
        self.llog = []
        self.rlog = []

    def update_size(self):
        st = struct.pack('HHHH', 0, 0, 0, 0)
        ret = fcntl.ioctl(0, termios.TIOCGWINSZ, st)
        self.rows, self.columns, _hp, _wp = struct.unpack('HHHH', ret)
        self.log_width = self.columns / 2 - 1

    def set_line_right(self, idx, line):
        while idx >= len(self.rlog):
            self.rlog.append('')
        self.rlog[idx] = line

    def get_split_lines(self, lines):
        chunked = []
        for line in lines:
            chunks = [line[i:i + self.log_width] for i in xrange(0, len(line), self.log_width)]
            chunked.extend(chunks)
        return chunked

    def refresh(self):
        self.update_size()
        sys.stdout.write('\033[1;1H')
        if len(self.llog) > self.rows:
            self.llog = self.llog[-self.rows:]
        if len(self.rlog) > self.rows:
            self.rlog = self.rlog[:self.rows]

        llines = self.get_split_lines(self.llog)
        rlines = self.get_split_lines(self.rlog)

        idx = self.rows - len(llines) - 1
        for r in xrange(self.rows - 1):
            if r < idx:
                sys.stdout.write(' ' * self.log_width)
            else:
                line = llines[r - idx]
                l = len(line)       # FIXME: account tab-formatted strings
                sys.stdout.write(line + ' ' * (self.log_width - l))
            sys.stdout.write(' | ')
            if r < len(rlines):
                sys.stdout.write(rlines[r])
            sys.stdout.write('\r\n')


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


args = sys.argv[1:]
name = args[0] if args else 'ashley'
interval_secs = float(args[1]) if len(args) > 1 else 1

# url_1 = 'http://getquote.icicidirect.com/trading_stock_quote.aspx?Symbol=%s' % name
# url_2 = 'https://secure.icicidirect.com/IDirectTrading/trading/trading_stock_bestbid.aspx?Symbol=%s' % name
url_1 = 'file:///home/wafflespeanut/Desktop/trading_stock_quote.aspx?Symbol=ashley'
url_2 = 'file:///home/wafflespeanut/Desktop/trading_stock_bestbid.aspx?Symbol=ashley'

last_share = 0
filename = name + datetime.now().strftime('-%Y-%m-%d')
watcher = Watcher()

while True:
    watcher.refresh()
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
        line = '[%s]: %s   %-5s %6s %10s  (%s, %s)' % \
               (g('DATE'), g('LAST TRADED TIME'), last_price, day_volume - last_share, day_volume, day_low, day_high)
        watcher.llog.append(line)

        idx = 116
        for i in range(5):      # 5 rows
            end = idx + 7 * offset      # 7 cols
            line = ' ' * 5 + ''.join(map(lambda i: '%-10s' % l2[i], range(idx, end + 1, offset))[:4])
            watcher.set_line_right(i, line)
            idx = end + 5

        with open(filename, 'a') as fd:
            fd.write(line + '\n')
    last_share = day_volume
    sleep(interval_secs)
