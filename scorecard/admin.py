from django.contrib import admin

from .models import Project

class ProjectAdmin(admin.ModelAdmin):
    list_display = ['geo', 'programme', 'title', 'status']
    search_fields = ['title']
    list_filter = ['status']

    class Meta:
        ordering = ['geo_code']

admin.site.register(Project, ProjectAdmin)
