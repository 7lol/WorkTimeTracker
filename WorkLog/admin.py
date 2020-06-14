from django.contrib import admin
from .models import Position, Employee, Month, Project, Activity, EmployeeHoursEnrollment
# Register your models here.
admin.site.register(Position)
admin.site.register(Employee)
admin.site.register(Month)
admin.site.register(Project)
admin.site.register(Activity)
admin.site.register(EmployeeHoursEnrollment)
