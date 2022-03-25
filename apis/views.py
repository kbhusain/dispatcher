import re
from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
User = get_user_model()
from rest_framework import viewsets
from django.views.debug import ExceptionReporter
from rest_framework import permissions
from apis.serializers import UserSerializer, GroupSerializer
from r2p.models import onePerson, Requesteditem, REQ_STATUS_CHOICES, itemStatusType, itemType
from django.http import JsonResponse
from django.db.models import Q
import json
from django.core import serializers


class CustomExceptionReporter(ExceptionReporter):
    def get_traceback_data(self):
        data = super().get_traceback_data()
        # ... remove/add something here ...
        return data

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = get_user_model().objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]




def getItemsForDialogBoxes(request, *args, **kwargs):
    ptype = 'PRODUCER'
    producers = onePerson.objects.filter(person_type=ptype).values()
    status    =  itemStatusType.objects.all().values()
    types     =  itemType.objects.all().values()
    r_id     =  int( kwargs.get('r_id', -1))
    if (r_id > 0):
        requests  = Requesteditem.objects.filter(req_id=r_id).values()
        for r in requests:
            request   = r
    else: 
        request   = None;

    results = { 
        'producers' : [x for x in producers  ], 
        'status'    : [x for x in status ], 
        'itype'     : [x for x in types ],
        'request'   : request
        } 
   # print ("getItemsForDialogBoxes", len(results))
    return JsonResponse(results)

def allPeople(request, *args, **kwargs):
    ptype = kwargs.get('ptype', 'REQUESTER')
    data = onePerson.objects.filter(person_type=ptype).values()
    persons =  [x for x in data  ]
    results = { 
        'data' : persons, 
        } 
   # print ("allPeople ....", len(results))
    return JsonResponse(results)



def allItems(request, *args, **kwargs):
    ptype = kwargs.get('ptype', 'REQUESTER')
    persons = onePerson.objects.all().values()
    data = Requesteditem.objects.all().values()
    results = getReturnItems(data,persons)
    return JsonResponse(results)


def getReturnItems(data, opersons):
    
    persons = onePerson.objects.all().values()
    types     =  itemType.objects.all().values()
    for x in data:
        if x['req_item_type'] == None: 
            print("NONE! ", x['req_id'])

    itypes = { x['itm_id']:  x['itm_Type'] for x in types }
    people = {}
    for p in persons:  
        people[p['person_id']] = p['person_firstname'] + " " + p['person_lastname']; 

    items =  [x for x in data  ]
    for x in data: 
        status = x["req_status"]
        if status == None:
            print("Status == ", status)
            status = 1
        x['req_statusStr'] = REQ_STATUS_CHOICES[status][1]; 
        x['req_requester_name'] = people.get(x['req_requester_id'], "Unassigned") 
        x['req_provider_name']  = people.get(x['req_assigned_to'], "Unassigned")
        x['req_typeStr'] = itypes.get(x['req_item_type'],"Other")
        

    results = { 
        'data' : items, 
        } 
    return results



def getTasksForProducer(request, *args, **kwargs):
    v_id = kwargs.get('v_id', -1)
  #  print("Assigned to ID --", v_id)
    data = Requesteditem.objects.filter(req_assigned_to=v_id).values()
    persons = onePerson.objects.filter(person_id=v_id).values()

    results = getReturnItems(data,persons)
    results ['requester'] = [ x for x in persons ]
        
    return JsonResponse(results)


def getAllRequestsByRequester(request, *args, **kwargs):
    r_id = kwargs.get('r_id', -1)
    print("Requests by ID --", r_id)
    data = Requesteditem.objects.filter(req_requester__person_id=r_id).values()
    persons = onePerson.objects.filter(person_id=r_id).values()
 
    results = getReturnItems(data,persons)
    results ['requester'] = [ x for x in persons ]

    print(results)
        
    return JsonResponse(results)


def getAllRequestsByRequestId(request, *args, **kwargs):
    r_id = kwargs.get('r_id', -1)
  #  print("Requests by ID --", r_id)
    persons = onePerson.objects.filter(person_id=r_id).values()
    data = Requesteditem.objects.filter(req_id=r_id).values()

    results = getReturnItems(data,persons)
    results ['requester'] = [ x for x in persons ]
        
    return JsonResponse(results)


def getAllRequestsByAssignee(request, *args, **kwargs):
    r_id = kwargs.get('r_id', -1)
    avail = kwargs.get('avail', 0)
    persons = onePerson.objects.all().values()
    types     =  itemType.objects.all().values()
    itypes = { x['itm_id']:  x['itm_Type'] for x in types }
    people = {}
    for p in persons:  
        people[p['person_id']] = p['person_firstname'] + " " + p['person_lastname']; 


    data  = Requesteditem.objects.filter(req_assigned_to=r_id).values()
    available_tasks =  [ ]
    if avail: 
        #also  = Requesteditem.objects.exclude(req_assigned_to=r_id).values()
        also  = Requesteditem.objects.filter(req_assigned_to=None).values()
        for item in also: 
            status = item["req_status"]
            if status == None: status = 1
            item['req_statusStr'] = REQ_STATUS_CHOICES[status][1]; 
            r_id = item['req_requester_id']
            requesters = onePerson.objects.filter(person_id=r_id).values()
            requester  = requesters[0]; 
            r_id = item['req_requester_id']
            item['req_fullname'] = requester['person_firstname'] + " " + requester['person_lastname']

            item['req_requester_name'] = people.get(item['req_requester_id'], "Unassigned") 
            item['req_provider_name']  = people.get(item['req_assigned_to'], "Unassigned")
            item['req_typeStr'] = itypes.get(item['req_item_type'],"Other")

        available_tasks =  [ x for x in also] 


    for item in data: 
        status = item["req_status"]
        if status == None:
           # print("Status == ", status)
            status = 1
        item['req_statusStr'] = REQ_STATUS_CHOICES[status][1]; 
        r_id = item['req_requester_id']
        requesters = onePerson.objects.filter(person_id=r_id).values()
        requester  = requesters[0]; 
        r_id = item['req_requester_id']
        item['req_fullname'] = requester['person_firstname'] + " " + requester['person_lastname']
        item['req_requester_name'] = people.get(item['req_requester_id'], "Unassigned") 
        item['req_provider_name']  = people.get(item['req_assigned_to'], "Unassigned")
        item['req_typeStr'] = itypes.get(item['req_item_type'],"Other")

    person = onePerson.objects.filter(person_id=r_id).values()
    results = { 'data' : [ x for x in data  ],
        'requester': [ x for x in person ], 
        'available': available_tasks,
        } 
    return JsonResponse(results)




def createOnboardRequests(request, *args, **kwargs):
    r_id = int(kwargs.get('r_id', -1))
    all_types     =  itemType.objects.all()
    # itypes = { x['itm_id']:  x['itm_Type'] for x in types }
    onep = onePerson.objects.filter(person_id=r_id)[0]

    for qs in all_types: 
        desc = "{itype}".format(itype=qs.itm_Type)
        obj = Requesteditem(req_requester=onep, 
                req_item_type=qs.itm_id, req_quantity= 1, req_status=0, 
                req_title = qs.itm_Type, req_description=desc)
        obj.save()

    results = { 'response': 'Created items. ', 
                 } 
    return JsonResponse(results)


def assignRequest(request, *args, **kwargs):
    r_id = int(kwargs.get('r_id', -1))
    v_id = int(kwargs.get('p_id', -1))

    print(" -- id ", v_id, r_id)
    response = ""

    data = Requesteditem.objects.filter(req_id=r_id)

   

    for dm in data:
        dm.req_assigned_to = v_id; 
        print("---- Assigning to --- ", v_id, r_id)
        response += str(r_id)
        dm.save() 
    results = { 'response': response, 
                 } 
    return JsonResponse(results)


def unassignRequest(request, *args, **kwargs):
    r_id = kwargs.get('r_id', -1)
    data = Requesteditem.objects.filter(req_id=r_id)

    response = "Unassigning " + str(r_id) 

    for dm in data: 
        dm.req_assigned_to = None; 
        response += "After Unassigning " + str(dm.req_assigned_to)
        dm.save() 
    results = { 'response': response, 
                } 
 
    return JsonResponse(results)


def getPersonById(request, *args, **kwargs):
    pid = kwargs.get('pid', 'REQUESTER')
    data = onePerson.objects.filter(person_id=pid).values()
    results = { 'data' : [x for x in data  ]} 
    return JsonResponse(results)

##
##
##
def getIDbyEmail(request, *args, **kwargs):
    email = kwargs.get('email','None')
    data = onePerson.objects.filter(Q(person_email__contains=email) | \
            Q(person_workemail__contains=email)).values()
    results = { 'data' : [ str(x) for x in data  ]} 
    return JsonResponse(results)

def getIDbyPhoneNumber(request, *args, **kwargs):
    phonenumber = kwargs.get('phonenumnber', 'None')
    data = onePerson.objects.filter(Q(person_cellphone__contains=phonenumber) | \
            Q(person_workphone__contains=phonenumber) | \
            Q(person_homephone__contains=phonenumber)).values()
    results = { 'data' : [ str(x) for x in data  ]} 
    return JsonResponse(results)
