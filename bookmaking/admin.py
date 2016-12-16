from django.contrib import admin
from .models import User1, Horse



class MyAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'contacts', 'bank_account')
    search_fields = ['name']

class HorseAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'pic')
    search_fields = ['name']

admin.site.register(User1, MyAdmin)
admin.site.register(Horse, HorseAdmin)