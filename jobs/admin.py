from django.contrib import admin
from .models import Job, Project


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'date_range', 'order')
    list_editable = ('order',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'order')
    list_editable = ('order',)
