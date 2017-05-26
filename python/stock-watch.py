from argparse import ArgumentParser
from datetime import datetime
from threading import Thread
from time import sleep

import argparse, fcntl, select, struct, sys, termios, tty, urllib2

CURSOR_TOP_LEFT = '\033[1;1H'
RED = '\033[91m'
GREEN = '\033[92m'
COLOR_NULL = '\033[0m'

class Watcher(object):
    def __init__(self):
        self.fd = sys.stdin.fileno()
        self.old = termios.tcgetattr(self.fd)
        tty.setraw(sys.stdin)
        self.llog = []
        self.rlog = []

    def exit(self):
        termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old)
        exit()

    def update_size(self):
        st = struct.pack('HHHH', 0, 0, 0, 0)
        ret = fcntl.ioctl(0, termios.TIOCGWINSZ, st)
        self.rows, self.columns, _hp, _wp = struct.unpack('HHHH', ret)
        self.log_width = self.columns / 2 - 1

    def set_line_right(self, idx, line):
        while idx >= len(self.rlog):
            self.rlog.append(' ' * (self.log_width - 1))
        self.rlog[idx] = line

    def get_split_lines(self, lines):
        chunked = []
        for line in lines:
            chunks = [line[i:i + self.log_width] for i in xrange(0, len(line), self.log_width)]
            chunked.extend(chunks)
        return chunked

    def refresh(self):
        self.update_size()
        sys.stdout.write(CURSOR_TOP_LEFT)
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
                sys.stdout.write(line + ' ' * (self.log_width - len(line)))
            sys.stdout.write(' | ')
            if r < len(rlines):
                sys.stdout.write(rlines[r] + ' ' * (self.log_width - len(rlines[r]) - 1))
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


parser = ArgumentParser(description='Watch live updates from NSE')
parser.add_argument('--market', '-m', type=str, default='ashley',
                    help='market to watch (default: ashley)')
parser.add_argument('--quantity', '-q', type=int, default=0,
                    help='total shares buy/sell (default: null)')
parser.add_argument('--cost', '-c', type=float, default=0.0,
                    help='value of share during buy/sell time (default: null)')
parser.add_argument('--type', '-t', choices=['buy', 'sell'], default='null',
                    help='buy/sell (default: null)')
parser.add_argument('--day', '-d', choices=['intra', 'deliver'], default='null',
                    help='day on which the trade will take place (default: null)')
parser.add_argument('--interval', '-i', type=float, default=1,
                    help='sleep interval in seconds (default: 1)')
parser.add_argument('--output', '-o', action='store_true', default=False,
                    help='output to log file')

args = parser.parse_args()
name, amount, cost, interval_secs = args.market, args.quantity, args.cost, args.interval

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
        max_len = 0
        x_shift, y_shift = int(0.15 * watcher.columns), int(0.08 * watcher.rows)
        rows, cols = 5, 7
        for i in range(rows):
            end = idx + cols * offset
            line = ' ' * x_shift + ''.join(map(lambda i: '%-10s' % l2[i], range(idx, end + 1, offset))[:4])
            if len(line) > max_len:
                max_len = len(line)
            watcher.set_line_right(i + y_shift + 1, line)
            idx = end + 5

        watcher.set_line_right(y_shift - 1, ' ' * x_shift + '-' * (max_len - x_shift - 5))
        watcher.set_line_right(rows + y_shift + 2, ' ' * x_shift + '-' * (max_len - x_shift - 5))

        watcher.set_line_right(watcher.rows / 3, '=' * (watcher.log_width - 1))

        y_shift = watcher.rows / 3 + 3
        opp_act = 'buy' if args.type == 'sell' else 'sell' if args.type == 'buy' else 'null'

        if args.day == 'intra':
            intra_frac = 0.06
            trade_worth = amount * cost
            curr_worth = amount * last_price
            diff = (last_price - cost) if args.type == 'buy' else (cost - last_price)
            blocked = trade_worth * intra_frac
            brokerage = (trade_worth + curr_worth) * 0.0005
            tax = brokerage * 0.14
            stt = curr_worth * 0.00025
            stamp = (trade_worth + curr_worth) * 0.00006
            sebi = (trade_worth + curr_worth) * (0.00002 + 0.0000231)
            net_comm = brokerage + tax + stt + stamp + sebi
            final = curr_worth - net_comm
            earned = amount * diff
            on_hand = earned - net_comm
            res = 'gain' if on_hand > 0 else 'loss' if on_hand < 0 else 'neutral'

            watcher.set_line_right(y_shift,
                                   name.upper() + \
                                   ' (%s) %s%s%s' % \
                                   (args.day.title(), RED if res == 'loss' else GREEN, '[%s]' % res.upper(), COLOR_NULL))
            watcher.set_line_right(y_shift + 2, '%-4s %s at %s' % (args.type.upper(), amount, cost))
            watcher.set_line_right(y_shift + 3, '%-4s %s at %s' % (opp_act.upper(), amount, last_price))
            watcher.set_line_right(y_shift + 5, 'DIFF: %s' % diff)

            stuff = [('Stock worth', trade_worth), ('Current worth', curr_worth), ('Blocked amount', blocked),
                     ('Cash earned', earned), ('Commission', -net_comm), ('Cash on hand', on_hand)]
            for i, (label, value) in enumerate(stuff):
                watcher.set_line_right(y_shift + 7 + i, '%-15s : %10.2f' % (label, value))
        elif args.day == 'deliver':
            pass

        if args.output:
            with open(filename, 'a') as fd:
                fd.write(line + '\n')

    last_share = day_volume
    inp, out, err = select.select([sys.stdin], [], [], interval_secs)       # listens to key input in the sleep interval
    for i in inp:
        if i == sys.stdin:
            watcher.exit()
