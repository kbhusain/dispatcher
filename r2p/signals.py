

from http.client import INSUFFICIENT_STORAGE
from accounts.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver  
from .models import onePerson, PERSON_PROD , PERSON_REQ

@receiver(post_save,sender=User)
def createPerson(sender,instance, created, **kwargs):
    if created:
        onePerson.objects.create(user=instance)

@receiver(post_save,sender=User)
def savePerson(sender, instance, **kwargs):
    instance.oneperson.person_firstname = instance.first_name
    instance.oneperson.person_lastname = instance.last_name
    instance.oneperson.person_email = instance.email
    instance.oneperson.person_djangoid = instance.email
    instance.oneperson.person_cellphone = instance.phone_number 
    if instance.is_producer:
        instance.oneperson.person_type = PERSON_PROD
    else: 
        instance.oneperson.person_type = PERSON_REQ
    
    instance.oneperson.save()
