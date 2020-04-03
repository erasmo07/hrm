from django.contrib import admin
from hrm.collaborator import models

# Register your models here.

admin.site.register(models.Position)
admin.site.register(models.OrganizationUnit)
admin.site.register(models.PersonalArea)
admin.site.register(models.Level)
admin.site.register(models.Collaborator)