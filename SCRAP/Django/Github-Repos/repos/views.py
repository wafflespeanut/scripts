import urllib,ast
from django.http import HttpResponse

def repo_list(user):
    page=urllib.urlopen("https://api.github.com/users/"+user+'/repos')
    stuff=page.read().replace('false','False').replace('true','True').replace('null','None')
    d=ast.literal_eval(stuff)
    if not d: return None
    return [i['name'] for i in d]

def search_form(request):
    with open('search_form.html','r') as file: data=file.readlines()
    return HttpResponse(''.join(data))

def search(request):
    if not len(request.GET['q']): return HttpResponse('Empty search query!')
    user=request.GET['q']; repo=repo_list(user)
    if repo==None: return HttpResponse("User doesn't exists!")
    l=['https://github.com/%s/%s'%(user,repo[i]) for i in range(len(repo))]
    m=['<tr><td>%s.</td><td><a href="%s">%s</a></td></tr>'%(i+1,l[i],j) for i,j in enumerate(repo)]
    s='<table>%s</table>'%'\n'.join(m)
    stuff='''
        <!DOCTYPE html>
        <html>
            <head><title>Search results</title></head>
            <body>%s
            <div align=center>%s</div>
            </body>
        </html>
        '''%('<br>'*5,s)
    return HttpResponse(stuff)
