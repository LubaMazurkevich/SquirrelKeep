from django.shortcuts import render, get_object_or_404, redirect
from .models import List, ListItem, Category, Tag
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

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
    categories = Category.objects.all()
    tags = Tag.objects.all()

    if request.method == 'POST':
        title = request.POST.get('title')
        category_id = request.POST.get('category')
        new_category_name = request.POST.get('new_category')
        tags_str = request.POST.get('tags')
        items_list = request.POST.getlist('items[]')
        if title:
            new_list = List.objects.create(title=title, user=request.user)
            if category_id:
                category = get_object_or_404(Category, id=category_id)
                new_list.category = category
            elif new_category_name:
                category, created = Category.objects.get_or_create(name=new_category_name.strip())
                new_list.category = category
            new_list.save()
            if tags_str:
                tag_names = [name.strip() for name in tags_str.split(',') if name.strip()]
                for name in tag_names:
                    tag, created = Tag.objects.get_or_create(name=name)
                    new_list.tags.add(tag)
            for item_text in items_list:
                item_text = item_text.strip()
                if item_text:
                    ListItem.objects.create(list=new_list, text=item_text)
            return redirect('list_detail', list_id=new_list.id)

    return render(request, 'lists/list.html', {
        'lists': lists,
        'current_list': lst,
        'all_checked': all_checked,
        'categories': categories,
        'tags': tags,
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


