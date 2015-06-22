from django.http import HttpResponse, Http404
from datetime import datetime, timedelta
from django.template import Template, Context

def time(request,offset=5.5):               # Just got into Django!
    try:
        offset = float(offset)
    except Exception:
        raise Http404()
    now = datetime.now() + timedelta(hours = offset)
    values = request.META.items()
    meta = ['<tr><td>%s</td><td>%s</td></tr>' % (k, v) for k, v in sorted(values)]
    t = Template('''
            <!DOCTYPE html>
            <html>
                <body>%s
                <div align=center>
                <p><font face="verdana" size="4">(Offset: %s hours)</font></p>
                <font face="courier" color="red" size="5"><strong>Usage</strong>: /time/(offset)</font>
                <h2>{{day}}/{{month}}/{{year}} ({{time}})</h2><br><br></div>
                <font face="arial" size="5">[Metadata]</font><br><br>
                </body>
            </html>
        ''' % ('<br>' * 2, offset))
    meta = '<table>%s</table>' % '\n'.join(meta)
    c = Context({'day': now.day, 'month': now.month, 'year': now.year, 'time': now.time()})
    return HttpResponse(t.render(c) + meta)
