from django.db import models

# Create your models here.
import os
from django.urls import reverse_lazy
from django.utils import timezone
from accounts.models import User

PERSON_DONOR = 'DONOR'
PERSON_PROD  = 'PRODUCER'
PERSON_REQ   = 'REQUESTER' 

PERSON_TYPES = (
    ('', str('Choose Person Type')),
    (PERSON_DONOR, str('Donor')),
    (PERSON_PROD, str('Volunteer or Producer')),
    (PERSON_REQ, str('Recipient or Requester'))
)

PERSON_MALE = 0
PERSON_FEMALE = 1

PERSON_GENDER = (
    ('', str('Choose Person Gender')),
    (str(PERSON_MALE), str('Male')),
    (str(PERSON_FEMALE), str('Female')),
 

)


class onePerson(models.Model):
    person_id = models.AutoField(db_column='person_ID', primary_key=True)  # Field name made lowercase.
    person_title = models.CharField(db_column='person_Title', max_length=50, blank=True, null=True)  # Field name made lowercase.
    person_type = models.CharField(db_column='person_Type', choices=PERSON_TYPES, max_length=10 ,default='REQUESTER', blank=True, null=True)  # Field name made lowercase.
    person_djangoid = models.CharField(db_column='person_DjangoID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    person_firstname = models.CharField(db_column='person_FirstName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    person_middlename = models.CharField(db_column='person_MiddleName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    person_lastname = models.CharField(db_column='person_LastName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    person_suffix = models.CharField(db_column='person_Suffix', max_length=50, blank=True, null=True)  # Field name made lowercase.
    person_address1 = models.CharField(db_column='person_Address1', max_length=50, blank=True, null=True)  # Field name made lowercase.
    person_address2 = models.CharField(db_column='person_Address2', max_length=50, blank=True, null=True)  # Field name made lowercase.
    person_city = models.CharField(db_column='person_City', max_length=50, blank=True, null=True)  # Field name made lowercase.
    person_state = models.CharField(db_column='person_State', max_length=50, blank=True, null=True)  # Field name made lowercase.
    person_zip = models.CharField(db_column='person_Zip', max_length=50, blank=True, null=True)  # Field name made lowercase.
    person_origincountry = models.CharField(db_column='person_OriginCountry', max_length=50, blank=True, null=True)  # Field name made lowercase.
    person_homephone = models.CharField(db_column='person_HomePhone', max_length=30, blank=True, null=True)  # Field name made lowercase.
    person_workphone = models.CharField(db_column='person_WorkPhone', max_length=30, blank=True, null=True)  # Field name made lowercase.
    person_cellphone = models.CharField(db_column='person_CellPhone', max_length=30, blank=True, null=True)  # Field name made lowercase.
    person_email = models.CharField(db_column='person_Email', max_length=50, blank=True, null=True)  # Field name made lowercase.
    person_workemail = models.CharField(db_column='person_WorkEmail', max_length=50, blank=True, null=True)  # Field name made lowercase.
    person_gender = models.CharField(db_column='person_Gender', choices=PERSON_GENDER, max_length=10, default='M', null=True)  # Field name made lowercase.
    person_dob = models.DateField(auto_now=False,blank=True,null=True)
    person_familysituation = models.CharField(db_column='person_familysituation',verbose_name=  'Family Situation', max_length=255, blank=True, null=True)  # Field name made lowercase.
    person_dateemployed = models.DateField(db_column='person_DateEmployed',verbose_name=  'Date Employed', blank=True, null=True)  # Field name made lowercase.
    person_datedrvlic = models.DateField(db_column='person_DateDrvLic',verbose_name=  'Date on License', blank=True, null=True)  # Field name made lowercase.
    person_datedeactivated = models.DateField(db_column='person_DateDeactivated',verbose_name=  'Date Removed', blank=True, null=True)  # Field name made lowercase.
    person_cashdonated = models.FloatField(db_column='person_cashDonated',verbose_name=  'Cash Donated', blank=True, null=True)  # Field name made lowercase.
    person_notes = models.TextField(db_column='person_notes',verbose_name=  'Notes', blank=True, null=True)  # Field name made lowercase.
    person_numkids =models.IntegerField(db_column='person_numkids',verbose_name=  'Num of kids', blank=True, null=True)
    person_agekids = models.CharField(db_column='person_agekids',verbose_name=  'Kids ages', max_length=32, blank=True, null=True)  # Field name made lowercase.
    person_spouse =models.CharField(db_column='person_spouse',verbose_name=  'Spouse Name',max_length=32, blank=True, null=True)
    person_certificates = models.CharField(db_column='person_certificates',verbose_name=  'Certificates', max_length=255, blank=True, null=True)  # Field name made lowercase.
    person_education = models.CharField(db_column='person_education',verbose_name=  'Education', max_length=64, blank=True, null=True)  # Field name made lowercase.
    person_languages = models.CharField(db_column='person_languages',verbose_name=  'Languages', max_length=255, blank=True, null=True)  # Field name made lowercase.
    person_ssn = models.CharField(db_column='person_ssn',verbose_name=  'Soc. Sec. Num', max_length=32, blank=True, null=True)  # Field name made lowercase.
    person_snap = models.CharField(db_column='person_snap',verbose_name=  'SNAP Card Num', max_length=32, blank=True, null=True)  # Field name made lowercase.
    person_arrivaldate = models.DateField(db_column='person_ArrivalDate',verbose_name=  'Arrival Date', blank=True, null=True)  # Field name made lowercase.
    person_vehicleinfo = models.CharField(db_column='person_vehicleinfo',verbose_name=  'Vehicle owned info', max_length=255, blank=True, null=True)  # Field name made lowercase.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)   
    person_enteredby = models.PositiveSmallIntegerField(db_column='person_EnteredBy', blank=True, null=True)  # Field name made lowercase.
    person_editedby = models.PositiveSmallIntegerField(db_column='person_EditedBy', blank=True, null=True)  # Field name made lowercase.
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    
    class Meta:
        managed = True
        db_table = 'oneperson'

    def get_absolute_url(self):
        return  reverse_lazy("person_list")



POOR = 1
BELOW_AVERAGE = 2
AVERAGE = 3
GOOD = 4
EXCELLENT = 5

SCORE_CHOICES = (
    ('', str('Choose your score')),
    (POOR, str('1 - Very Poor')),
    (BELOW_AVERAGE, str('2 - Below Average')),
    (AVERAGE, str('3 - Average')),
    (GOOD, str('4 - Good')),
    (EXCELLENT, str('5 - Excellent'))
)


class Donateditem(models.Model):
    don_id = models.AutoField(db_column='don_ID', primary_key=True)  # Field name made lowercase.
    don_title = models.CharField(max_length=128)
    don_item_type = models.CharField(max_length=64)
    don_status = models.IntegerField(choices=SCORE_CHOICES,default=3,null=True,blank=True)
    don_given_to = models.PositiveIntegerField(db_column='don_given_to',null=True)  # Field name made lowercase.
    don_donated_by = models.IntegerField(db_column='don_donated_by',null=True)  # Field name made lowercase.
    don_requester_id = models.IntegerField(db_column='don_requester_ID')  # Field name made lowercase.
    don_caseworker_id = models.IntegerField(db_column='don_caseworker_ID')  # Field name made lowercase.
    don_multibuy = models.SmallIntegerField()
    don_description = models.TextField(blank=True, null=True)
    don_actualprice = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    don_estprice = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    don_minimum = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    don_materialvalue = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    don_enteredby = models.PositiveSmallIntegerField(db_column='don_EnteredBy')  # Field name made lowercase.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)   
    don_neededbydate = models.DateField(db_column='don_NeededByDate')  # Field name made lowercase.
    don_filledbydate = models.DateField(db_column='don_FilledByDate')  # Field name made lowercase.
    don_notes = models.TextField(default="", max_length=255, blank=True, null=True)
    don_upload = models.ImageField(upload_to ='uploads/')
    
    class Meta:
        managed = False
        db_table = 'Donateditem'

    def get_absolute_url(self):
        return  reverse_lazy("donated_item")



REQ_STATUS_CHOICES = (
    (0, str('Open')),
    (1, str('Initiated')),
    (2, str('Approved')),
    (3, str('Rejected')),
    (4, str('Cancelled')),
    (5, str('Assigned')),
    (6, str('Progressing')),
    (7, str('Completed')),
    (8, str('Closed'))
)

class Requesteditem(models.Model):
    req_id = models.AutoField(db_column='req_ID', primary_key=True)  # Field name made lowercase.
    req_requester = models.ForeignKey(onePerson,on_delete=models.CASCADE)  # Field name made lowercase.
    req_item_type = models.IntegerField(blank=True, null=True)
    req_status = models.IntegerField(choices=REQ_STATUS_CHOICES,default=0,blank=True, null=True)
    req_assigned_to = models.IntegerField( blank=True, null=True)   
    req_quantity = models.SmallIntegerField(blank=True, null=True)
    req_title = models.CharField(max_length=128, blank=True, null=True)
    req_description = models.TextField(blank=True, null=True)
    req_actualprice = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    req_estprice = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    req_minimum = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    req_time_taken = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    req_materialvalue = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    req_enteredby = models.IntegerField(db_column='req_EnteredBy', blank=True, null=True)  # Field name made lowercase.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)   
    req_neededbydate = models.DateField(db_column='req_NeededByDate', blank=True, null=True)  # Field name made lowercase.
    req_filledbydate = models.DateField(db_column='req_FilledByDate', blank=True, null=True)  # Field name made lowercase.
    req_notes = models.TextField( max_length=255, blank=True, null=True)
    req_upload = models.ImageField(upload_to ='uploads/', blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'requesteditem'


    def get_absolute_url(self):
        return  reverse_lazy("requested_list")



class itemStatusType(models.Model):
    itm_id = models.AutoField(db_column='itm_ID', primary_key=True)  # Field name made lowercase.
    itm_Status = models.CharField(db_column='itm_Status', max_length=64, blank=True, null=True)  # Field name made lowercase.


    class Meta:
        managed = True
        db_table = 'itemStatusType'

    def get_absolute_url(self):
        return  reverse_lazy("item_status_type_list")


class itemType(models.Model):
    itm_id = models.AutoField(db_column='itm_ID', primary_key=True)  # Field name made lowercase.
    itm_Type = models.CharField(db_column='itm_Type', max_length=64, blank=True, null=True)  # Field name made lowercase.


    class Meta:
        managed = True
        db_table = 'itemType'

    def get_absolute_url(self):
        return  reverse_lazy("item_type_list")

