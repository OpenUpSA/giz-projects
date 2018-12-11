from django.contrib import admin
from django import forms
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget
#from django_extensions.admin import ForeignKeyAutocompleteAdmin

from .models import Project, Programme, Geography, ProjectResource, CleanForeignKeyWidget




class GeoForm(forms.ModelForm):
    geo = forms.ModelChoiceField(queryset=Geography.objects.order_by('name'))

    class Meta:
        model = Geography
        fields = '__all__'

class ProjectAdmin(ImportExportModelAdmin):
    resource_class = ProjectResource
    list_display = ['geo', 'programme', 'title', 'status']
    search_fields = ['title']
    list_filter = ['status', 'programme', 'geo__name']
    autocomplete_fields = ['geo']
    form = GeoForm

#ForeignKeyAutocompleteAdmin

class ProgrammeAdmin(admin.ModelAdmin):
    pass

admin.site.register(Project, ProjectAdmin)
admin.site.register(Programme, ProgrammeAdmin)
