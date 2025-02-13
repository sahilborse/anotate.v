from django.contrib import admin

# Register your models here.
from .models import DataEntry, Annotation,HighlightedText

admin.site.register(DataEntry )
admin.site.register(Annotation)
admin.site.register(HighlightedText)