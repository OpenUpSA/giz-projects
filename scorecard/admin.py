import tablib
from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget
from import_export.fields import Field

from .models import Project, Programme, Geography


class CleanForeignKeyWidget(ForeignKeyWidget):
    def clean(self, value, row, *args, **kwargs):
        value = value.strip()
        return super(CleanForeignKeyWidget, self).clean(value, row, *args, **kwargs)

class ProjectResource(resources.ModelResource):

    programme = Field(
        column_name='programme',
        attribute='programme',
        widget=CleanForeignKeyWidget(Programme, 'name')
    )

    geo = Field(
        column_name='municipality',
        attribute='geo',
        widget=CleanForeignKeyWidget(Geography, 'geo_code')
    )

    class Meta:
        model = Project
        export_order = ('id', 'programme', 'geo', 'title', 'status', 'area_of_work', 'mode_of_delivery', 'partner', 'agenda', 'm_and_e', 'contact', 'email')

class ProjectAdmin(ImportExportModelAdmin):
    resource_class = ProjectResource
    list_display = ['geo', 'programme', 'title', 'status']
    search_fields = ['title']
    list_filter = ['status']

class ProgrammeAdmin(admin.ModelAdmin):
    pass

admin.site.register(Project, ProjectAdmin)
admin.site.register(Programme, ProgrammeAdmin)
