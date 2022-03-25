from django.contrib import admin
from .models import onePerson,   Donateditem, Requesteditem
from .models import itemType, itemStatusType 
# Register your models here.

admin.site.register(onePerson) 
admin.site.register(Donateditem)
admin.site.register(Requesteditem)
admin.site.register(itemType)
admin.site.register(itemStatusType)

# Register your models here.
