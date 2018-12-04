import tablib
from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget
from import_export.fields import Field

from .models import Project, Programme, Geography


class ProgrammeForeignKeyWidget(ForeignKeyWidget):
    def render(self, value, obj=None):
        import pdb; pdb.set_trace()

class ProjectResource(resources.ModelResource):

    programme = Field(
        column_name='programme',
        attribute='programme',
        widget=ForeignKeyWidget(Programme, 'name')
    )

    geo = Field(
        column_name='municipality',
        attribute='geo',
        widget=ForeignKeyWidget(Geography, 'geo_code')
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
