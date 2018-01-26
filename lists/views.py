from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ValidationError

from lists.forms import ItemForm, ExistingListItemForm
from lists.models import Item, List

def home_page(request):
    return render(request, 'home.html', {'form': ItemForm()})

def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        form.save(for_list=list_)
        return redirect(list_)
    else:
        return render(request, 'home.html', {"form": form})


def view_list(request, list_id):

    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)
    if request.method == 'POST':
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save(for_list=list_)
            return redirect(list_)
    return render(request, 'list.html', {"form": form, 'list': list_})


def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)
    text = request.POST['item_text']
    text = text.strip()
    if text:
        Item.objects.create(text=text, list=list_)
        return HttpResponseRedirect(f'/lists/{list_id}/')
    else:
        return view_list(request, list_id, "You can't have an empty list item")