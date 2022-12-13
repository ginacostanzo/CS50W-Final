from django.contrib import admin

from .models import User, Trip, List, Tag, Photo
# Register your models here.

admin.site.register(User),
admin.site.register(Trip),
admin.site.register(List),
admin.site.register(Tag),
admin.site.register(Photo)