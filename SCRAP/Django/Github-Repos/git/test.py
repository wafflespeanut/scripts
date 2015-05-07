from django.http import HttpResponse,Http404
from datetime import datetime,timedelta
from django.template import Template,Context

def time(request,offset=5.5):               # Django-101
    try: offset=float(offset)
    except Exception: raise Http404()
    now=datetime.now()+timedelta(hours=offset)
    values=request.META.items(); values.sort(); meta=[]
    t=Template('''
            <!DOCTYPE html>
            <html>
                <body>%s
                <div align=center>
                <h3>(Offset: %s hours)</h3>
                Usage: <strong>/time/</strong>(offset)
                <h2>{{ day }}/{{ month }}/{{ year }} ({{ time }})</h2><br><br></div>
                </body>
            </html>
        '''%('<br>'*2,offset))
    for k,v in values: meta.append('<tr><td>%s</td><td>%s</td></tr>'%(k,v))
    meta='<table>%s</table>'%'\n'.join(meta)
    c=Context({'day': now.day,'month': now.month,'year': now.year,'time': now.time()})
    return HttpResponse(t.render(c)+meta)
