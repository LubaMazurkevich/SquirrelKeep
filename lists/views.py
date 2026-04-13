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
def list_view(request):
    show_all_lists = request.GET.get('all') == '1'

    # only current user lists
    base_lists_qs = List.objects.filter(parent=None, user=request.user)
    total_lists = base_lists_qs.count()
    has_more_lists = total_lists > 5

    if show_all_lists:
        lists = base_lists_qs
    else:
        lists = base_lists_qs[:5]

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
        'form': form,
        'has_more_lists': has_more_lists,
        'show_all_lists': show_all_lists,
    })


@login_required
def list_detail_view(request, list_id):
    lst = get_object_or_404(List, id=list_id, user=request.user)
    all_checked = lst.items.exists() and not lst.items.filter(checked=False).exists()
    edit_mode = request.GET.get('edit') == '1'
    form = ListCreateForm(instance=lst) if edit_mode else None
    return render(request, 'lists/list_detail.html', {
        'current_list': lst,
        'all_checked': all_checked,
        'form': form,
        'edit_mode': edit_mode,
    })


@login_required
@require_POST
def edit_list(request, list_id):
    lst = get_object_or_404(List, id=list_id, user=request.user)
    form = ListCreateForm(request.POST, instance=lst)
    if form.is_valid():
        form.save()
        raw_items = request.POST.getlist('items[]')
        cleaned_items = [text.strip() for text in raw_items if text.strip()]

        # Keep existing checked states where possible by updating items by position.
        existing_items = list(lst.items.order_by('id'))
        for index, text in enumerate(cleaned_items):
            if index < len(existing_items):
                item = existing_items[index]
                if item.text != text:
                    item.text = text
                    item.save(update_fields=['text'])
            else:
                ListItem.objects.create(list=lst, text=text)

        if len(existing_items) > len(cleaned_items):
            for item in existing_items[len(cleaned_items):]:
                item.delete()

    return redirect('list_detail', list_id=list_id)

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


