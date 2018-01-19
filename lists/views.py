from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ValidationError

from lists.models import Item, List

def home_page(request):
    return render(request, 'home.html')

def new_list(request):
    list_ = List.objects.create()
    item = Item(text=request.POST['item_text'], list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        errors = "You can't have an empty list item"
        return render(request, 'home.html', {"errors": errors})
    return redirect(f'/lists/{list_.id}/')


def view_list(request, list_id, errors=None):
    list_ = List.objects.get(id=list_id)
    if request.method == 'POST':
        try:
            item = Item(text=request.POST['item_text'], list=list_)
            item.full_clean()
            item.save()
            return redirect(f'/lists/{list_.id}/')
        except ValidationError:
            errors = "You can't have an empty list item"

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