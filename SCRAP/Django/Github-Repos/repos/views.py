import urllib,ast
from django.http import HttpResponse

def user_details(user):
    page=urllib.urlopen("https://api.github.com/search/users?q="+user)
    stuff=page.read().replace('false','False').replace('true','True')
    d=ast.literal_eval(stuff)
    if not d: return None

def search_form(request):
    with open('search_form.html','r') as file: data=file.readlines()
    return HttpResponse(''.join(data))

def search(request):
    if not len(request.GET['q']): m='Empty search query!'
    elif 'q' in request.GET: m='You searched for: %s'%request.GET['q']
    return HttpResponse(m)
