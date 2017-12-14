from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from lists.models import Item

def home_page(request):
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return HttpResponseRedirect('/')
    return render(request, 'home.html', {
        'items': Item.objects.all(),
    })
