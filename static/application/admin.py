from django.contrib import admin
from application.models import *
from django.contrib import admin
from .models import enquiry_table, enquiry_table_1

@admin.register(enquiry_table)
class EnquiryTableAdmin(admin.ModelAdmin):
    list_per_page = 25  # Limits rows per page
    list_display = ('name', 'email', 'subject', 'date')  # Avoid loading too many fields


# Register your models here.

# admin.site.register(enquiry_table)

@admin.register(enquiry_table_1)
class EnquiryTableAdmin(admin.ModelAdmin):
    list_per_page = 25  # Limits rows per page
    list_display = ('name', 'email', 'subject', 'date')  # Avoid loading too many fields

