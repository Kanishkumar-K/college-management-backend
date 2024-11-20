from django.contrib import admin
from .models import Faculty, Subject

class FacultyAdmin(admin.ModelAdmin):
    list_display = ['faculty_name', 'email', 'subject']
    
    def save_model(self, request, obj, form, change):
        if obj.password:
            obj.set_password(obj.password) 
        super().save_model(request, obj, form, change)

admin.site.register(Faculty, FacultyAdmin)  # Add faculty from django admin

admin.site.register(Subject)
