from django.urls import path , re_path
from .views import vwRequesters, vwProducers
from .views import vwAllPeopleAfterLogin, vwAllPeopleAfterSignup 
from .views import showRecipients,  cancelRequest, refreshRequesterPage
from .views import vwItems,vwItemsByRequester,vwItemsByProducer 
from .views import RequiredItemDetail, RequiredItemList,PersonsDetail,PersonsList , DonatedItemList, DonatedItemDetail
 

app_name = 'r2p'

urlpatterns = [
  # path('allPeople/<str:ptype>/<int:p_id>/', vwAllPeople.as_view(), name='allPeople'),
  #  path('allPeople/<str:ptype>/', vwAllPeople.as_view(), name='allPeople'),
    path('allPeopleAfterSignup/<str:ptype>/<int:p_id>/', vwAllPeopleAfterSignup.as_view(), name='allPeopleAfterSignup'),
    path('allPeopleAfterLogin/', vwAllPeopleAfterLogin.as_view(), name='allPeopleAfterLogin'),
    path('requesters/', vwRequesters.as_view(), name='requesters'),
    path('producers/', vwProducers.as_view(), name='producers'),
    path('items/', vwItems.as_view(), name='items'),
    path('itemsByRequester/<int:p_id>/', vwItemsByRequester.as_view(), name='itemsByRequester'),
    path('cancelRequest/<int:r_id>/', cancelRequest, name='cancelRequest'),
    path('refreshRequesterPage/<int:p_id>/', refreshRequesterPage, name='refreshRequesterPage'),

    path('itemsByProducer/<int:p_id>/', vwItemsByProducer.as_view(), name='itemsByProducer'),
    path('producers/<str:fname>/', vwProducers.as_view()),
    path('showRecipients/', showRecipients, name='showRecipients'),
    #path('signup/', SignUpView.as_view(), name='signup'), 
 
    #path('makeDemoData', makeDemoData, name="makeDemoData"),
      ### From rest framework ###
    path('personsList', PersonsList.as_view() , name="personsList" ),
    path('requiredItemList', RequiredItemList.as_view() , name="requiredItemList" ),
    path('donatedItemList', DonatedItemList.as_view() , name="donatedItemList" ),
    path('personsDetail/<int:pk>/', PersonsDetail.as_view() , name="personsDetail"),
    path('requiredItemDetail/<int:pk>/', RequiredItemDetail.as_view() , name="requiredItemDetail"),
    path('donatedItemDetail/<int:pk>/', DonatedItemDetail.as_view() , name="donatedItemDetail"),
    
    
]