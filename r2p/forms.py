from django import forms
from .models import onePerson, Requesteditem, Donateditem


class OnePersonForm(forms.ModelForm):
    class Meta:
        model = onePerson
        fields = [
                    "person_title",
                    "person_type",
                    "person_djangoid",
                    "person_firstname",
                    "person_middlename",
                    "person_lastname",
                    "person_address1",
                    "person_address2",
                    "person_city",
                    "person_state",
                    "person_zip",
                    "person_origincountry",
                    "person_homephone",
                    "person_workphone",
                    "person_cellphone",
                    "person_email",
                    "person_workemail",
                    "person_gender",
                    "person_dob"]

class OnePersonDelete(forms.ModelForm):
    class Meta:
        model = onePerson
        fields = []
        

class RequestedItemForm(forms.ModelForm):
    class Meta: 
        model: Requesteditem
        fields = [ "__all__"]


class DonatedItemForm(forms.ModelForm):
    class Meta: 
        model: Donateditem
        fields = [ "__all__"]