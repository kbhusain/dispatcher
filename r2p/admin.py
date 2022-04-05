from django.contrib import admin
from .models import onePerson,   Requesteditem # Donateditem, 
from .models import itemType, itemStatusType 
# Register your models here.

#admin.site.register(onePerson) 
#admin.site.register(Donateditem)
#admin.site.register(Requesteditem)
admin.site.register(itemType)
admin.site.register(itemStatusType)


@admin.register(Requesteditem)
class RequesteditemAdmin(admin.ModelAdmin):
    list_display = ['req_requester', 'req_title', 'req_neededbydate']
    list_filter =  ['req_requester', 'req_title', 'req_neededbydate']
    search_fields = ['req_title', 'req_description']
    # prepopulated_fields 
    # raw_id_fields
    # data_hierarchy
    # ordering

@admin.register(onePerson)
class onePersonAdmin(admin.ModelAdmin):
    list_display = ['person_firstname', 'person_lastname', 'person_email', 'person_cellphone']
    list_filter =  ['person_email', 'person_cellphone']
    search_fields = ['person_firstname', 'person_lastname', 'person_email', 'person_cellphone']

# Register your models here.
  