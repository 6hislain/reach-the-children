from django.contrib import admin
from .models import Sponsor, School, Student, Visit, Payment, SchoolHistory

# Register your models here.
admin.site.register(Visit)
admin.site.register(School)
admin.site.register(Sponsor)
admin.site.register(Student)
admin.site.register(Payment)
admin.site.register(SchoolHistory)
