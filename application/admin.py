from django.contrib import admin
from .models import enquiry_table, enquiry_table_1


@admin.register(enquiry_table)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'email',
        'phone',
        'people',
        'status',
        'date',
    )
    list_filter = ('status', 'date')
    search_fields = ('name', 'email')
    ordering = ('-date',)
    list_per_page = 25


@admin.register(enquiry_table_1)
class ContactAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'email',
        'phone',
        'subject',
        'date',
    )
    search_fields = ('name', 'email', 'subject')
    ordering = ('-date',)
    list_per_page = 25
