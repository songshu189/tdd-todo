from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from lists.models import Item

def home_page(request):
    return render(request, 'home.html')

def new_list(request):
    Item.objects.create(text=request.POST['item_text'])
    return HttpResponseRedirect('/lists/the-only-list-in-the-world/')

def view_list(request):
    return render(request, 'list.html', {'items': Item.objects.all(),})
