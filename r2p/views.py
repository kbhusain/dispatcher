

from django.contrib.auth import get_user_model

from django.http import HttpResponse
from django.views import View # generic
from xml.etree.ElementInclude import include
from django.shortcuts import render, redirect 
from django.urls import reverse, reverse_lazy
from rest_framework import generics, status
from rest_framework.response import Response
from r2p.models import onePerson, itemType,  Requesteditem, itemStatusType, Donateditem
from r2p.models import PERSON_DONOR , PERSON_PROD, PERSON_REQ , REQ_STATUS_CHOICES
from django.core import serializers
from .serializers import onePersonSerializer, requestedItemSerializer, donatedItemSerializer
from django.http import HttpResponse, Http404

import json

basicTasksForNewRefuguee = [
    "Other",
    "Furniture",
    "Kitchen, household items",
    "Social Security card." ,
    "SNAP benefits",
    "SIM card",
    "Basic essentials packet",
    "Clothing",
    "Laptop Computer",
    "Job Assistance",
    "Tuition assistance ",
    "Car driving training.",
    "English Language Classes "]




# Create your views here.

def index(request,  *args, **kwargs):
    ptype = kwargs.get('ptype','REQUESTER')

    persons = onePerson.objects.filter(person_type=ptype)
    context = {
            'query_results': persons
            }
    return render(request, 'base.html', context=context)

        
class PersonsList(generics.ListCreateAPIView):
    queryset = onePerson.objects.all();
    serializer_class = onePersonSerializer

class PersonsDetail(generics.RetrieveUpdateDestroyAPIView): 
    queryset = onePerson.objects.all();
    serializer_class = onePersonSerializer


class RequiredItemList(generics.ListCreateAPIView):
    queryset = Requesteditem.objects.all();
    serializer_class = requestedItemSerializer
 

class RequiredItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Requesteditem.objects.all();
    serializer_class = requestedItemSerializer


class DonatedItemList(generics.ListCreateAPIView):
    queryset = Donateditem.objects.all();
    serializer_class = donatedItemSerializer
 

class DonatedItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Donateditem.objects.all();
    serializer_class = donatedItemSerializer





 
    # def get_item(self,pk):
    #     try:
    #         return Requesteditem.objects.get(pk=pk) 
    #     except:
    #         raise Http404

    # def put(self,request,pk,format=None):
    #     print("Putting ...", pk)
    #     person = self.get_item(pk)
        
    #     serializer = requestedItemSerializer(person,data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     else: 
    #         print("Not valid....", serializer.errors)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
##
# Normal class views. 
##

# from django.contrib.auth.forms import UserCreationForm





class vwAllPeopleAfterLogin(View):
    def get(self, request, *args, **kwargs):

        print("vwAllPeopleAfterSignup", kwargs)
        User = get_user_model()
        thisUser = User.objects.filter(email=request.user.email)[0]
        ptype = thisUser.oneperson.person_type
        p_id  = thisUser.oneperson.person_id

        if p_id == None: 
            persons = onePerson.objects.filter(person_type=ptype)
        else: 
            persons = onePerson.objects.filter(person_type=ptype).filter(person_id=p_id)
        #p_json = serializers.serialize('json',persons)
        context = {
            'query_results': persons
            }
        if ptype == 'PRODUCER':
            return redirect(reverse_lazy('r2p:itemsByProducer', kwargs={'p_id':p_id}))
        if ptype == 'REQUESTER':
            return redirect(reverse_lazy('r2p:itemsByRequester', kwargs={'p_id':p_id}))
        return render(request, "base.html", context=context)



class vwAllPeopleAfterSignup(View):
    def get(self, request, *args, **kwargs):

        print("vwAllPeopleAfterLogin", kwargs)
        User = get_user_model()
    
        ptype = kwargs.get('ptype','REQUESTER')
        p_id  = kwargs.get('p_id',None)
 

        if p_id == None: 
            persons = onePerson.objects.filter(person_type=ptype)
        else: 
            persons = onePerson.objects.filter(person_type=ptype).filter(person_id=p_id)
        #p_json = serializers.serialize('json',persons)
        context = {
            'query_results': persons
            }
        if ptype == 'PRODUCER':
            return redirect(reverse_lazy('r2p:itemsByProducer', kwargs={'p_id':p_id}))
        if ptype == 'REQUESTER':
            return redirect(reverse_lazy('r2p:itemsByRequester', kwargs={'p_id':p_id}))
        return render(request, "base.html", context=context)

class vwProducers(View):
    def get(self, request, *args, **kwargs):
        try:
            fname = kwargs['fname']
            persons = onePerson.objects.filter(person_type='PRODUCER').filter(person_firstname=fname)
        except: 
            print("Empty kwargs for fname") 
            persons = onePerson.objects.filter(person_type='PRODUCER')
        results = []
        for x in persons:
            #print(x.person_firstname)
            results.append(x)
        # xstr = [ "<tr><td>{fname}</td><td>{lname}</td> </tr>".format(fname=x.person_firstname,\
        #     lname=x.person_lastname)  for x in persons ]
        # # <view logic>
        # #return HttpResponse('result: <br> ' + "\n".join( xstr ))
        # tbl = "<table><th><td>First</td><td>Last</td></th>" + \
        #      "\n".join( xstr ) + "</table>"

        context = {
            'PageHeader' : "Page Header",
            'query_results': results}
        return render(request, "base.html", context=context)

    #def get(self, request, *args, **kwargs):
    #    return render(request, "index.html")
## --------------------------------------------------------------------------------------------
##                          The view shown to show all requesters. 
## --------------------------------------------------------------------------------------------
class vwRequesters(View):
    def get(self, request, *args, **kwargs):
        persons = onePerson.objects.filter(person_type='REQUESTER')
        results = []
        for x in persons:
            #print (x.person_firstname)
            results.append(x)
        context = {
            'PageHeader' : "Requesters",
            'query_results': results}
        return render(request, "base.html", context=context)

## --------------------------------------------------------------------------------------------
##                          The view shown to requesters. 
## --------------------------------------------------------------------------------------------
class vwItemsByRequester(View):
    def get(self, request, *args, **kwargs):
        try:
            p_id = kwargs['p_id']
            persons = onePerson.objects.filter(person_id=p_id).values()
        except: 
            context = {
            'PageHeader'  : "Requester not found",
             }
            #("!!!! --- kwargs ", kwargs)
            return render(request, "vwRefugees.html", context=context)
        person = persons[0]
        #  print("Person", person)
        statuses = itemStatusType.objects.all().values(); 
        names = [ x['itm_Status']  for x in statuses ] 
        items = Requesteditem.objects.filter(req_requester=p_id).values()
        for item in items: 
            xstr = names[ item['req_status'] ] 
            item['req_statusStr'] = xstr; 
            #print(item['req_assigned_to'])
            a_id = item['req_assigned_to']
            assigned_name = "None"
            if a_id : 
                try: 
                    assignee = onePerson.objects.filter(person_id=a_id).values()
                    
                    for ap in assignee: 
                        
                        assigned_name = ap['person_firstname'] + " " + ap['person_lastname'] 
                except:
                    assigned_name = "None"
            item['req_assigned_name'] = assigned_name; 


        # for x in items:
        #     print(x.req_requester)
        #     results[x.req_requester.req_id] = 1
        context = {
            'PageHeader'  : "Requested Items",
            'RefugeeName' : person['person_firstname'] + " " + person['person_lastname'], 
            'Person'      : person, 
            'items':    items 
        } 
        return render(request, "vwRefugees.html", context=context)


## --------------------------------------------------------------------------------------------
##                          The view shown to providers. 
## --------------------------------------------------------------------------------------------
def cancelRequest(request, *args, **kwargs):
    r_id = kwargs.get('r_id', -1)
    response = ''
    data = Requesteditem.objects.filter(req_id=r_id)
    if len(data) < 0: 
        response += "bad r_id"
    data[0].req_status = REQ_STATUS_CHOICES[-1][0]
    data[0].save() 
    p_id = data[0].req_requester.person_id; 
    #("P ID", p_id, data[0] )
    return redirect(reverse_lazy('r2p:itemsByRequester', kwargs={'p_id':p_id}))

def refreshRequesterPage(request, *args, **kwargs):
    p_id = kwargs.get('p_id', -1)
    #print("P ID", p_id )
    return redirect(reverse_lazy('r2p:itemsByRequester', kwargs={'p_id':p_id}))

## --------------------------------------------------------------------------------------------
##                          The view shown to providers. 
## --------------------------------------------------------------------------------------------
class vwItemsByProducer(View):
    def get(self, request, *args, **kwargs):
        try:
            p_id = kwargs['p_id']
            persons = onePerson.objects.filter(person_id=p_id).values()
        except: 
            context = {
            'PageHeader'  : "Requester not found",
             }
           # print("!!!! --- kwargs ", kwargs)
            return render(request, "vwRefugees.html", context=context)

        context = get_assignments_context(p_id) 
        return render(request, "vwProducers.html", context=context)



##
def get_assignments_context(p_id):
        persons = onePerson.objects.filter(person_id=p_id).values()
        person = persons[0]

       # print("Person", person)
        statuses = itemStatusType.objects.all().values(); 
        names = [ x['itm_Status']  for x in statuses ] 
        #items = Requesteditem.objects.filter(req_assigned_to=p_id).values()
        all_items = Requesteditem.objects.all().values()

        my_items = [] 
        all_open_items = []
        for item in all_items: 
            if  item['req_assigned_to'] == p_id or item['req_status'] == 0: 
                xstr = names[ item['req_status'] ] 
                item['req_statusStr'] = xstr ; 
                r_id = item['req_requester_id']
                requesters = onePerson.objects.filter(person_id=r_id).values()
                requester  = requesters[0]; 
                r_id = item['req_requester_id']
                item['req_fullname'] = requester['person_firstname'] + " " + requester['person_lastname']
            
                if item['req_assigned_to'] == p_id: 
                    my_items.append(item)
                else: 
                    all_open_items.append(item)

        context = {
            'PageHeader'  : "Assigned Items",
            'AssigneeName' : person['person_firstname'] + " " + person['person_lastname'], 
            'Person'      : person, 
            'item_list'   :   my_items,
            'all_items_list': all_open_items
        } 


        return context; 





class vwItems(View):
    def get(self, request, *args, **kwargs):
        items = Requesteditem.objects.all()
        results = {}
        # for x in items:
        #     print(x.req_requester)
        #     results[x.req_requester.req_id] = 1
        context = {
            'PageHeader' : "Requested Items",
            'query_results': results.keys() 
        } 
        return render(request, "base.html", context=context)



def showRecipients(request):
    title = "Kamran Husain"
    persons = onePerson.objects.filter(person_type='REQUESTER')
    xstr = [ "<p> {fname} </p>".format(fname=x.person_firstname) for x in persons ]
    clist = "\n".join(xstr)
    parms = { 
        'title': title, 
        'tableOfNames': clist
    }
    return render(request,'r2p/ex_recipientList.html', parms)


##
# --------------------  
##
# sample= {
#         "person_id": 1,
#         "person_title": "kamran husain",
#         "person_type": "2",
#         "person_djangoid": "kbhusain",
#         "person_firstname": "Kamran",
#         "person_middlename": "",
#         "person_lastname": "Husain",
#         "person_suffix": "",
#         "person_address1": "5482 HighFlyer Hills Trail",
#         "person_address2": "",
#         "person_city": "Frisco",
#         "person_state": "Texas",
#         "person_zip": "75036",
#         "person_origincountry": "United States",
#         "person_homephone": "15127668061",
#         "person_workphone": "",
#         "person_cellphone": "",
#         "person_email": "khusain62@yahoo.com",
#         "person_workemail": "khusain62@yahoo.com",
#         "person_gender": "0",
#         "person_dob": null,
#         "created_at": "2022-02-10T16:24:02.386754Z",
#         "updated_at": "2022-02-10T16:24:02.386754Z",
#         "person_enteredby": null,
#         "person_editedby": null
#     }
##



def makeStatusTypeoData(request, deletefirst='False'):


    items = itemType.objects.all().delete()
    for x in basicTasksForNewRefuguee: 
        item = itemType()
        item.itm_Type = x
        item.save() 

    itemStatusType.objects.all().delete() 
    for x in REQ_STATUS_CHOICES: 
        status = x[1] 
        item = itemStatusType()
        item.itm_id = int(x[0])
        item.itm_Status = x[1]
        item.save() 
  
    html = "<html><body>It is now created</body></html>" 
    return HttpResponse(html)





def makeDemoDataRequest(request, deletefirst='False'):
    # Create 10 requesters;
    html = "<html><body>It is now created</body></html>" 
    return HttpResponse(html)


def makeDemoData():
    myUser = get_user_model(); 
    for x in range(5):
        rfname = "rfirstname_{num}".format(num=x+1)
        rlname = "rlastname_{num}".format(num=x+1)    
        remail  = 'e_rlastname_{num}@abc.com'.format(num=x+1)  
        user1 = myUser()
        user1.is_requester = True; 
        user1.is_producer = False;  
        user1.is_staff     = False;
        user1.set_password('1234')
        user1.email = remail 
        user1.first_name = rfname; 
        user1.last_name  = rlname;   
        user1.phone_number = "469-555-12%02d" %(x+1)
        user1.save()

    
    for x in range(5):
        rfname = "pfirstname_{num}".format(num=x+1)
        rlname = "plastname_{num}".format(num=x+1)    
        remail  = 'e_plastname_{num}@abc.com'.format(num=x+1)  
        user1 = myUser()
        user1.is_requester = False; 
        user1.is_producer = True; 
        user1.is_staff     = False;
        user1.set_password('1234')
        user1.email = remail 
        user1.first_name = rfname; 
        user1.last_name  = rlname;   
        user1.phone_number = "214-555-12%02d" %(x+1)
        user1.save()

    
    for x in range(3):
        rfname = "pfStaff{num}".format(num=x+1)
        rlname = "plStaff_{num}".format(num=x+1)    
        remail  = 'e_staffer_{num}@abc.com'.format(num=x+1)  
        user1 = myUser()
        user1.is_requester = False; 
        user1.is_producer = True; 
        user1.is_staff     = True;
        user1.set_password('1234')
        user1.email = remail 
        user1.first_name = rfname; 
        user1.last_name  = rlname;   
        user1.phone_number = "972-555-12%02d" %(x+1)
        user1.save()


    return 1