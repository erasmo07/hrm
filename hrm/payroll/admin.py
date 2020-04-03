from django.contrib import admin
from hrm.payroll import models

# Register your models here.

admin.site.register(models.TypePayroll)
admin.site.register(models.LawDiscount)
admin.site.register(models.PayrollConfiguration)
