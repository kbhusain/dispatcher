from django.urls import path , re_path
from .views import UserViewSet, GroupViewSet

from .views import getAllRequestsByRequester, getAllRequestsByRequestId, getAllRequestsByAssignee
from .views import assignRequest,unassignRequest, getPersonById, getTasksForProducer, getItemsForDialogBoxes
from .views import getIDbyPhoneNumber, getIDbyEmail, allItems, allPeople, createOnboardRequests

app_name = 'apis'

urlpatterns = [
    path('allItems', allItems , name="allItems"),    
    path('allPeopleByType/<str:ptype>', allPeople , name="allPeopleByType"),
    path('getTasksForProducer/<int:v_id>/', getTasksForProducer, name="getTasksForProducer" ),
    path('getIDbyPhoneNumber/<str:phonenumber>/', getIDbyPhoneNumber , name="getIDbyPhoneNumber"),
    path('getIDbyEmail/<str:email>/', getIDbyEmail, name="getIDbyEmail" ),
    path('getAllRequestsByRequestId/<int:r_id>',getAllRequestsByRequestId, name="getAllRequestsByRequestId"),
    path('getAllRequestsByRequester/<int:r_id>',getAllRequestsByRequester, name="getAllRequestsByRequester"),
    path('getAllRequestsByAssignee/<int:r_id>/<int:avail>/',getAllRequestsByAssignee, name="getAllRequestsByAssignee"),
    path('assignRequest/<str:r_id>/<str:p_id>/',assignRequest, name="assignRequest"),
    path('unassignRequest/<int:r_id>/',unassignRequest, name="unassignRequest"),
    path('getPersonById/<int:r_id>',getPersonById, name="getPersonById"),
    path('getItemsForDialogBoxes/<str:r_id>', getItemsForDialogBoxes , name="getItemsForDialogBoxes"),    
    path('createOnboardRequests/<int:r_id>',createOnboardRequests, name="createOnboardRequests"),


]