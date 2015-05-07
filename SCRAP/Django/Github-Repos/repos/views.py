import urllib,ast
from django.http import HttpResponse

def repo_list(user):
    page=urllib.urlopen("https://api.github.com/users/"+user+'/repos')
    stuff=page.read().replace('false','False').replace('true','True').replace('null','None')
    d=ast.literal_eval(stuff)
    if not d: return False
    elif 'message' in d: return None
    return [i['name'] for i in d]

def search_form(request):
    with open('search_form.html','r') as file: data=file.readlines()
    return HttpResponse(''.join(data))

def search(request):
    if not len(request.GET['q']): s='Empty search query!'
    else: user=request.GET['q']; repo=repo_list(user)
    if repo==False: s="<h2>User doesn't have any repositories (yet)!</h2>"
    elif repo==None: s="<h2>User doesn't exists!</h2>"
    else:
        link=['https://github.com/%s/%s'%(user,repo[i]) for i in range(len(repo))]
        m=['<tr><td>%s.</td><td><a href="%s">%s</a></td></tr>'%(i+1,link[i],j) for i,j in enumerate(repo)]
        s='''<p style="padding:20px;">(%s has contributed to %d repositories...)</p>
                <table style="padding:50px;"> %s </table>'''%(user,len(m),'\n'.join(m))
    stuff='''
        <!DOCTYPE html>
        <html>
            <head><title>Search results...</title></head>
            <body> %s
            %s
            </body>
        </html>
        '''%('<br>'*3,s)
    return HttpResponse(stuff)
