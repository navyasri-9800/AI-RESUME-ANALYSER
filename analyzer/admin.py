from django.contrib import admin
from .models import (
    JobDescription, 
    Analysis
)
# Register your models here.
admin.site.register(JobDescription)
admin.site.register(Analysis)
