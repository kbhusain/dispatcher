from django.urls import path

from .views import SignUpView, UserCreateView, UserLoginView 


urlpatterns = [
    path('login/', UserLoginView.as_view(), name="login"),
    path('signup/', SignUpView.as_view(), name='signup'),           # Allows customization of fields. 
    path('signmeup/', UserCreateView.as_view(), name='signmeup'),
    
]