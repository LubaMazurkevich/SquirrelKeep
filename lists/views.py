import re
from urllib.parse import unquote_plus

from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from dal import autocomplete

from .models import List, ListItem, Category, Tag
from .forms import ListCreateForm


class CategoryAutocomplete(autocomplete.Select2QuerySetView):
    paginate_by = None
    create_field = "name"

    # Method for fetching categories based on user input, 
    # with support for creating new categories if they don't exist.
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Category.objects.none()
        qs = Category.objects.all().order_by('name')
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs


    def create_object(self, text):
        # DAL can send escaped values (for example %u044B%u044B for "ыы").
        # Normalize them before creating/fetching a category.
        decoded = unquote_plus(text or '')
        decoded = re.sub(r'%u([0-9A-Fa-f]{4})', lambda m: chr(int(m.group(1), 16)), decoded)
        clean_name = decoded.strip()
        if not clean_name:
            return None
        category, _ = Category.objects.get_or_create(name=clean_name)
        return category

    def has_add_permission(self, request):
        # Allow creating categories from autocomplete for any logged-in user.
        return request.user.is_authenticated


class TagAutocomplete(autocomplete.Select2QuerySetView):
    paginate_by = None
    create_field = "name"

    # Method for fetching tags based on user input 
    # and creating new tags if they don't exist.
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Tag.objects.none()
        qs = Tag.objects.all().order_by('name')
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs

    def create_object(self, text):
        decoded = unquote_plus(text or '')
        decoded = re.sub(r'%u([0-9A-Fa-f]{4})', lambda m: chr(int(m.group(1), 16)), decoded)
        clean_name = decoded.strip()
        if not clean_name:
            return None
        existing = Tag.objects.filter(name__iexact=clean_name).first()
        if existing:
            return existing
        return Tag.objects.create(name=clean_name)

    def has_add_permission(self, request):
        return request.user.is_authenticated


@login_required
def list_view(request, list_id=None):
    if list_id:
        lst = get_object_or_404(List, id=list_id, user=request.user)
        all_checked = lst.items.exists() and not lst.items.filter(checked=False).exists()
    else:
        lst = None
        all_checked = False
    # only current user lists
    lists = List.objects.filter(parent=None, user=request.user)
    form = ListCreateForm()

    if request.method == 'POST':
        form = ListCreateForm(request.POST)
        items_list = request.POST.getlist('items[]')
        if form.is_valid():
            new_list = form.save(commit=False)
            new_list.user = request.user
            new_list.save()
            form.instance = new_list
            form.save_m2m()
            for item_text in items_list:
                item_text = item_text.strip()
                if item_text:
                    ListItem.objects.create(list=new_list, text=item_text)
            return redirect('list_detail', list_id=new_list.id)

    return render(request, 'lists/list.html', {
        'lists': lists,
        'current_list': lst,
        'all_checked': all_checked,
        'form': form,
    })

@require_POST
def toggle_item(request, item_id):
    item = get_object_or_404(ListItem, id=item_id, list__user=request.user)
    item.checked = not item.checked
    item.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))

@require_POST
def toggle_all(request, list_id):
    lst = get_object_or_404(List, id=list_id, user=request.user)
    all_checked = all(item.checked for item in lst.items.all())
    for item in lst.items.all():
        item.checked = not all_checked
        item.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))


