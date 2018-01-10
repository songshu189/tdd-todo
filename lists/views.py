from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from lists.models import Item, List

def home_page(request):
    return render(request, 'home.html')

def new_list(request):
    text = request.POST['item_text']
    text = text.strip()
    if text:
        list_ = List.objects.create()
        Item.objects.create(text=text, list=list_)
        return HttpResponseRedirect(f'/lists/{list_.id}/')
    return render(request, 'home.html', {
        'errors': "You can't have an empty list item",
        })

def view_list(request, list_id, errors=None):
    list_ = List.objects.get(id=list_id)
    return render(request, 'list.html',
        {
        'list': list_,
        'errors': errors
        }
    )

def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)
    text = request.POST['item_text']
    text = text.strip()
    if text:
        Item.objects.create(text=text, list=list_)
        return HttpResponseRedirect(f'/lists/{list_id}/')
    else:
        return view_list(request, list_id, "You can't have an empty list item")