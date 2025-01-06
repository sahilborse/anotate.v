from django.contrib import admin

# Register your models here.
from .models import DataEntry, Annotation

admin.site.register(DataEntry )
admin.site.register(Annotation)