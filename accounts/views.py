from django.shortcuts import render

# Create your views here.
# accounts/views.py
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from .forms import RegisterForm
from django.urls import reverse_lazy
from django.views import generic


from django.contrib.auth import get_user_model
# from django.contrib.auth.forms import ReadOnlyPasswordHashField

User = get_user_model()



class UserLoginView(LoginView):
    model = get_user_model()
    template_name = 'registration/login.html'


    # def get_success_url(self) -> str:
    #     ptype = 'REQUESTER'
    #     if self.object.is_producer: ptype = 'PRODUCER'
    #     return reverse_lazy('r2p:allPeople', kwargs={'ptype': ptype,'p_id':self.object.oneperson.person_id} ) 

class SignUpView(generic.CreateView):
    model = get_user_model()
    form_class = RegisterForm 
    #success_url = reverse_lazy('r2p:allPeople')
    template_name = 'registration/signup.html'
# --------------------- Uses the fields in the class to get values 
    def get_success_url(self) -> str:
        ptype = 'REQUESTER'
        if self.object.is_producer: ptype = 'PRODUCER'
        return reverse_lazy('r2p:allPeople', kwargs={'ptype': ptype,'p_id':self.object.oneperson.person_id} ) 



# -------------------  Uses the "fields" paraameter to set the values
class UserCreateView(generic.CreateView):
    template_name = 'registration/signup.html'
    model =  get_user_model()
    fields = ['email', 'password', 'first_name', 'last_name',  'is_producer' ]
    #success_url =  reverse_lazy('r2p:allPeople', kwargs={'ptype': self.object.is_producer,'p_id':self.object.oneperson.person_id} ) 

    def get_success_url(self) -> str:
        ptype = 'REQUESTER'
        if self.object.is_producer: ptype = 'PRODUCER'
        return reverse_lazy('r2p:allPeopleAfterSignup', kwargs={ 'ptype': ptype,'p_id':self.object.oneperson.person_id} ) 


        # return super().get_success_url(


    def form_valid(self, form):
        form.instance.set_password(form.cleaned_data['password'])
        return super().form_valid(form)
        

