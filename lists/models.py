from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return self.name or "Без категории"

class Tag(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class List(models.Model):
    title = models.CharField(max_length=200)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='sublists', on_delete=models.CASCADE)
    related_lists = models.ManyToManyField('self', blank=True, symmetrical=False)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lists')

    def __str__(self):
        return self.title


class ListItem(models.Model):
    list = models.ForeignKey(List, related_name='items', on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    checked = models.BooleanField(default=False)

    def __str__(self):
        return self.text
