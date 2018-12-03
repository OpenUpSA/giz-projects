import tablib
from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Project

class ProjectResource(resources.ModelResource):

    class Meta:
        model = Project

ProjectResource = resources.modelresource_factory(model=Project)
project_resource = ProjectResource()
dataset = tablib.Dataset(['1', '', 'New book'], headers=['id', 'title', 'programme'])
result = project_resource.import_data(dataset, dry_run=True)
print(result.has_errors())

#class ProjectAdmin(admin.ModelAdmin):
#    list_display = ['geo', 'programme', 'title', 'status']
#    search_fields = ['title']
#    list_filter = ['status']
#
#    class Meta:
#        ordering = ['geo_code']
#

class ProjectAdmin(ImportExportModelAdmin):
    resource_class = ProjectResource
    list_display = ['geo', 'programme', 'title', 'status']
    search_fields = ['title']
    list_filter = ['status']

admin.site.register(Project, ProjectAdmin)
