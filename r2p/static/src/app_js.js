
function numOnly(selector){
  selector.value = selector.value.replace(/[^0-9]/g,'');
}


function refreshPersonCallback() {
  whatToDo = document.getElementById('query-results').getAttribute('refreshItems');
  console.log("Got reply back..,.", whatToDo);
  if (document.getElementById('query-results').getAttribute('refreshItems')==="true") {

      var sparms = document.getElementById('query-results').getAttribute('refreshItemsParms');
      var parms = sparms.split(",")
      var pid = parms[0]; 
      var url =  parms[1]; 
      var divname =  parms[2]; 
      console.log("Take Actions here..... [ fn, parms ] ", pid, url, divname)
      showRequestdetailsForPerson(pid,url,divname); // This is in actions.js file. 
  }

}


function refreshRequestModal() { 
  console.log("Refreshing page in refreshRequestModal...")
  var rid = document.getElementById('query-results').getAttribute('refresh_rid_after_edit');  // request id 
  var requester_id = document.getElementById('query-results').getAttribute('refresh_requester_id_after_edit');  // person (requestor or )
  var producer_id  = document.getElementById('query-results').getAttribute('refresh_producer_id_after_edit');  // person (requestor or )
 
  var fn  = document.getElementById('query-results').getAttribute('refresh-after-modal-edit');
  document.getElementById('query-results').setAttribute('refresh-after-modal-edit','');
  if (fn == 'refreshItemsDetailPage') {
    refreshItemsDetailPage(requester_id);
  }
  
  if (fn == 'refreshThisAssignmentPage') {
    refreshThisAssignmentPage(producer_id)
  }

    
  if (fn == 'refreshAllRequestsPage') {
    getAllItems('REQUESTER')
  }

  if (fn == 'refreshItemsForRequesterPage') {
    getAllPeople('REQUESTER')
  }

  $('#requestModal').modal('hide');

}



// PID is assignee  --- not requester. 
function refreshThisAssignmentPage(pid){ 
    showMyAssignments("available-task-list", "available-details-title"); 
}

/* 
Inputs: 
          Person ID --- for the person_id field in onePerson
*/

function detailsForPerson(pid) {
  xstr = "<p> ... Details about " + pid + " ... </p> "
  console.log(xstr)
  if (pid === null ) {
    return; 
  }

  var url = global_personDetail.replace('22',pid); 
  console.log(url) ;
  readJSON(url,function(err, data) {
        if (err != null) {
          console.error(err);
        } else { 
          console.log(data);
          showModalPerson('',data) ;
        }
      })
  }


  ///
function showMyAssignments(whereToShow, titleDivName ){ 
    var pid = global_personID; 
    var url = global_getAllRequestsByAssignee.replace('61',pid); 
    console.log(url) ;
    readJSON(url,function(err, data) {
        if (err != null) {
          console.error(err);
        } else { 
          console.log(data);

          createItemCards(pid,"query-results",data['data'], {'showUnassign': true, 'showAssign':false ,'showDelete': true });
          createItemCards(pid,whereToShow,data['available'],  {'showUnassign': true, 'showAssign':true , 'showDelete': true }) ;
          document.getElementById(titleDivName).innerHTML = '<center><button class="btn-dark" onclick="showAvailableTasks()">AvailableTasks</button></center>'
        }
      })
    }
// 'details-title'

function getPersonDetailForEdits(ppid) { 
  var url = global_personDetail.replace('22',ppid); 
  console.log(url) ;
  readJSON(url,function(err, data) {
        if (err != null) {
          console.error(err);
        } else { 
          console.log(data);
          showModalPerson('',data) ;
        }
      })

}


// /*

 
// /*
// Inputs: 
//     Person ID --- for the person_id field in onePerson
//     rtype  --- for REQUESTER, DONOR or PRODUCER
//     divname --- the div tag where the HTML output will go. 
//     Returns 
// */
function makeSelectOptions(ptype,input_id) {
  var url = global_allPeopleByType.replace('REQUESTER', ptype);
      console.log(url);
      readJSON(url,function(err, data) {
        if (err != null) {
          console.error(err);
        } else { 
          console.log(data);
            var hstr = ""; 
            var requestObject = document.getElementById('requestModal')
            selectItem  = requestObject.querySelector('#modalReq_assigned_to')
            //selectItem = $(input_id)
            for (var x=0;x<data.data.length; x++ ) {
              item = data.data[x]
              // option = document.createElement("option")
              // optionText = document.createTextNode(`${item.person_firstname} ${item.person_lastname}`);
              // option.appendChild(optionText) 
              // option.setAttribute("value",item.person_id);
              var xstr = `${item.person_firstname} ${item.person_lastname}`
              var vstr = `${item.person_id}`
              option = new Option(xstr,vstr);
              //option = `<option value="${item.person_id}">${item.person_firstname} ${item.person_lastname}</option>`
              selectItem.append(option);
            } 
            
        }
      })

}



function reportPersons(pType) {
  var url = global_personsList;
  var pid = global_personID
      readJSON(url,function(err, data) {
        if (err != null) {
          console.error(err);
        } else { 
         
          xstr = createPersonReport(pType, data)
          document.getElementById('query-results').innerHTML = xstr
          $("#basic-table").DataTable();
           
        }
      })

}



function createItemsTables(html_id,data,extras) {
    var hstr = "";  
    document.getElementById('pageHeader').innerHTML = '';
    var hstr = '<div> <table id="basic-items-table" class="sortable searchable table table-hover"  >';  
    hstr += `  <thead>
        <tr>
        <th>Details</th>
        <th>Requester</th>
        <th>Person</th>
          <th>Type</th>
          <th>Title</th> 
          <th>Status</th> 
          <th>Desc</th> 
          <th>Notes</th> 
          <th>Actions</th>
        </tr>
      </thead>
      <tbody id="basic-table-body">
    `;

    var pid = global_personID; 
    var btns = createSingleItemButtons(pid,item,extras); 
  
    var btn_unassign = btns[0]
    var btn_assign  = btns[1]
    var btn_cancel  = btns[2]
    var btn_delete  = btns[3]
  
    var notes = item.req_notes; 
    if (notes != null ) {
        if (notes.length > 12) {
          notes = notes.substring(0,12) + "..."
        }
      }

    for (var x=0;x<data.length; x++ ) {
        item = data[x]
        name = item.req_title; 
        xstr = `<tr>
          <td>
          <a href="javascript:editItemDetails('${item.req_requester_id}','${item.req_id}', 'admin', 'refreshAllRequestsPage')"> ${item.req_id}  
          </a>
          </td>
          <td> 
          <a href="javascript:" onclick='detailsForPerson(${item.req_requester_id}, "requester");'>
           ${item.req_requester_name} 
          </a>
          </td>
          <td>
          <a href="javascript:" onclick='detailsForPerson(${item.req_assigned_to}, "producer");'>
          ${item.req_provider_name}       </a>
          </td>


            <td>${item.req_typeStr}</td>
            <td>${item.req_title}</td>
            <td>${item.req_statusStr}</td>
            <td>${item.req_description}</td>
            <td>${notes}</td>
            <td> 
            ${btn_unassign}  ${btn_assign} ${btn_cancel} ${btn_delete}     
            </td>
        </tr> 
`
// 
        

        hstr += xstr; 
      }

      hstr += "</tbody></table></div>"
      document.getElementById(html_id).innerHTML = hstr;
      $('#' + html_id).sortable(); 
}

//-----------------------------------------------------------------------------------
// Returns all people of a particular type. 
//-----------------------------------------------------------------------------------
function getAllItems(iType) {
  console.log(iType);
  var url = global_apiAllItems;
  var pid = global_personID ; 
      readJSON(url,function(err, data) {
        if (err != null) {
          console.error(err);
        } else { 
          console.log(data);
          createItemsTables( 'query-results',data['data'],
             {'showUnassign': true, 'showAssign':false, 'showDelete': true }) ;
          document.getElementById('details').innerHTML = ''
          document.getElementById('details-title').innerHTML = ''
          $("#basic-items-table").DataTable();
        }
      })
}

function deleteThisRequest(r_id ) { 

  var result = confirm("Are you sure?");

  console.log("RESULT-", result)

  if (result === true ) {
        var csrftoken =  document.querySelector('[name=csrfmiddlewaretoken]').value
        var pid =  global_personID;
        var url1 = global_requiredItemDetail.replace('22',r_id);
        console.log(url1) ;
        $.ajax({
            url: url1,
            type: "DELETE",
            headers: { 'X-CSRFToken':  csrftoken },  
            contentType : 'application/json',
            success: function(data) { 
                var pid = global_personID;
                //refreshItemsDetailPage(pid);
                document.getElementById('query-results').setAttribute('refresh-after-modal-edit','refreshItemsForRequesterPage');
                refreshRequestModal();    
            }
        })
   }
}


function cancelThisRequest(r_id ) { 
    var csrftoken =  document.querySelector('[name=csrfmiddlewaretoken]').value 
    var pid = global_personID;
    var url1 = global_cancelRequest.replace('22',r_id);

    console.log(url1) ;
    $.ajax({
        url: url1,
        type: "POST",
        headers: { 'X-CSRFToken':  csrftoken },  
        contentType : 'application/json',
        success: function(data) { 
            var pid = global_personID;
            //refreshItemsDetailPage(pid);
            document.getElementById('query-results').setAttribute('refresh-after-modal-edit','refreshItemsForRequesterPage');
            refreshRequestModal();    
        }
    })
 }



function createSingleItemButtons(pid,item,extras) {


    var btn_assign = '';
    var assigntome = extras['showAssign']; 
    var unassign   = extras['showUnassign']
    var deletethis = extras['showDelete'];
    var cancelthis = false; 
  
   
    if ("showDelete" in extras) {
      deletethis = extras['showDelete']
    }
    btn_delete=''
    if (deletethis == true){
      btn_delete = `<a  class="button" href="javascript:deleteThisRequest(${item.req_id})" >Delete</a>`;
    }
  
    if ("showCancel" in extras) {
      cancelthis = extras['showCancel']
    }
    btn_cancel = ''
    if (cancelthis == true){
      btn_cancel = `<a class="button" href="javascript:cancelThisRequest(${item.req_id})" >Cancel</a>`;
    }
  
  
  
    
    if (assigntome === true ){
      btn_assign = `<a class="button" href="javascript:assignItemToPID(${item.req_id},${pid})" > ASSIGN TO ME</a>`;
    }
    if (unassign === false ){ 
      btn_unassign = '';
    } else {  
      btn_unassign = `<a class="button" href="javascript:unassignRequestForRID(${item.req_id})" >Unassign </a>          `
    }
  
    if  (item.req_assigned_to === null)  {
      btn_unassign = '';
    }
  
    return [ btn_unassign , btn_assign , btn_cancel , btn_delete ]
}


function createSingleItemCard(pid,item, extras)  
{
  
  var pid = global_personID; 
  var btns = createSingleItemButtons(pid,item,extras); 

  var btn_unassign = btns[0]
  var btn_assign  = btns[1]
  var btn_cancel  = btns[2]
  var btn_delete  = btns[3]

  var notes = item.req_notes; 
  if (notes != null ) {
      if (notes.length > 12) {
        notes = notes.substring(0,12) + "..."
      }
    }

  var xstr = `<div class="rcorners1 box"> 
              <ul class="nobullets">
              <h4 class="singleline">
                <a class="price" href="javascript:editItemDetails('${item.req_requester_id}','${item.req_id}', 'admin', 'refreshAllRequestsPage')"> ${item.req_id}  </a>
                </h4>
                <li>Assignee: 
                <a href="javascript:" onclick='detailsForPerson(${item.req_assigned_to}, "producer");'>
                <img src="${global_onePersonCheckIcon}" title="Assignee">${item.req_provider_name}
                </li>
              </a>
              <li>Requester: 
              <a href="javascript:" onclick='detailsForPerson(${item.req_requester_id}, "requester");'>
                <img src="${global_onePersonCheckIcon}" title="Requester">${item.req_requester_name}
              </a>
              </li>

              <li class="personinfo">Type: ${item.req_typeStr}</li>
              <li class="personinfo">What: ${item.req_title}</li>
              <li class="personinfo">Status: ${item.req_statusStr}</li>
              <li class="personinfo">Desc: ${item.req_description}</li>
              <li class="personinfo">Notes: ${notes}</li>
              <li>
              ${btn_unassign}  ${btn_assign} ${btn_cancel} ${btn_delete}
              </li>
              </ul>
            </div>
    `
    
  return xstr; 

}

//-----------------------------------------------------------------------------------
// Shows boxes of information in div named by html_id given the data; 
//-----------------------------------------------------------------------------------
function createItemCards(pid,html_id,data,extras) {
  var hstr = "";  
  document.getElementById('pageHeader').innerHTML = '';
  console.log("Item cards for ", pid)
  for (var x=0;x<data.length; x++ ) {
      item = data[x]
      name = item.req_title; 
      xstr = createSingleItemCard(pid,item,extras);    
      hstr += xstr; 
    }
    document.getElementById(html_id).innerHTML = hstr;
    $('#' + html_id).sortable(); 
    // DO NOT DO THIS --> $('#' + html_id).disableSelection(); 


}


//-----------------------------------------------------------------------------------
// Returns all people of a particular type. 
//-----------------------------------------------------------------------------------
function getAllPeople(ptype) { 
      var url = global_allPeopleByType.replace('REQUESTER', ptype);
      console.log(url);
      readJSON(url,function(err, data) {
        if (err != null) {
          console.error(err);
        } else { 
          console.log(data);
          createPersonCards('query-results',data) ;
          document.getElementById('details').innerHTML = ''
          document.getElementById('details-title').innerHTML = ''
          $("#basic-table").DataTable();
          
        }
      });
}


function assignItemToPID(req_id,pid) { 
    var csrftoken =  document.querySelector('[name=csrfmiddlewaretoken]').value
    var url1 = global_assignRequest.replace('1',pid).replace('0',req_id);
    console.log(url1) ;
    $.ajax({
        url: url1,
        type: "POST",
        headers: { 'X-CSRFToken':  csrftoken },  
        contentType : 'application/json',
        success: function(data) { 
            var pid = global_personID;
            refreshThisAssignmentPage(pid);
        }
    })
}

function unassignRequestForRID(req_id,pid) { 
    var csrftoken =  document.querySelector('[name=csrfmiddlewaretoken]').value
    var url1 = global_unassignRequest.replace('0',req_id);
    console.log(url1) ;
    $.ajax({
        url: url1,
        type: "POST",
        headers: { 'X-CSRFToken':  csrftoken },  
        contentType : 'application/json',
        success: function(data) { 
            var pid = global_personID;
            refreshThisAssignmentPage(pid);
        }
    })
}






//-----------------------------------------------------------------------------------
// Shows boxes of information in div named by html_id given the data; 
//-----------------------------------------------------------------------------------
function createPersonCards(html_id,data) {
  var hstr = '<div><table id="basic-table" class="table table-striped  table-hover" >';  
  hstr += `  <thead>
      <tr>
        <th>Person</th>
        <th>Address</th>
        <th>Actions</th> 
      </tr>
    </thead>
    <tbody>
  `
  document.getElementById('pageHeader').innerHTML = '';
  for (var x=0;x<data.data.length; x++ ) {
    item = data.data[x]
    url1 = global_getAllRequestsByRequester.replace('61',item.person_id);
    url2 = global_getAllRequestsByAssignee.replace('61',item.person_id);
    name = item.person_firstname + " " + item.person_lastname;
    console.log("Item ... " + name )


    var addRequestStr = '';
    if (item.person_type == 'REQUESTER') {
      addRequestStr = `<a class="btn-small" href="javascript:editItemForRefugee('${item.person_id}',-1)"><i class='fas fa-user-plus'></i>Create New Requests</a><br>
      <a class="btn-small" href="javascript:createOnboardRequests('${item.person_id}',-1)"><i class='fas fa-truck-loading'></i>Create On Board Items</a>
    `;
    }

      var xstr = `<tr>
                <td> <a href="javascript:" onclick='detailsForPerson(${item.person_id}, "producer");'> 
                <i class='fas fa-male' ></i>${item.person_id} 
                 <a   href="javascript:" onclick='showRequestdetailsForPerson(${item.person_id}, "${url1}", "details", "${name}");'>
                  Requests
                </a> 
                <a   href='javascript:showRequestdetailsForPerson(${item.person_id}, "${url2}", "details", "${name}");'>
                  Assignments
                </a> </td> 
                <td>
                <ul class="nobullets">
                <li class="personinfo">${item.person_firstname} ${item.person_lastname}</li>
                <li class="personinfo">${item.person_address1}, ${item.person_city} ${item.person_zip}</li>
                <li class="personinfo">${item.person_cellphone}</li>
                <li class="personinfo">${item.person_email}</li>
                </ul>
                </td>
                <td>
                ${addRequestStr}
                </td>
               
              </tr>
      `
      hstr += xstr; 
    }
    hstr += "</tbody></table></div>"
    document.getElementById(html_id).innerHTML = hstr;
     
    $("#basic-table").DataTable();
          
  // sorta(document.getElementById("basic-table"));
}


function createPersonReport(pType,data){

  var hstr = '<div> <table id="basic-table" class="sortable searchable table table-hover"  >';  
  hstr += `  <thead>
      <tr>
        <th>ID </th>
        <th>Person</th>
        <th>Address</th>
        <th>Phone</th> 
        <th>Email</th> 
      </tr>
    </thead>
    <tbody id="basic-table-body">
  `
  document.getElementById('pageHeader').innerHTML = 'Report on ' + pType;
  for (var x=0;x<data.length; x++ ) {
    item = data[x]
    url1 = global_getAllRequestsByRequester.replace('61',item.person_id);
    url2 = global_getAllRequestsByAssignee.replace('61',item.person_id);
    name = item.person_firstname + " " + item.person_lastname;
     
    if (item.person_type == pType) {

    var xstr = ` 
               <tr>        
                <td>${item.person_id}</td>
                <td>${item.person_firstname} ${item.person_lastname}</td>
                <td>${item.person_address1}, ${item.person_city} ${item.person_zip}</td>
                <td>${item.person_cellphone}</td>
                <td>${item.person_email}</td>
              </tr>
      `
      hstr += xstr; 
    }
  }
  hstr += "</tbody></table></div>"
  return hstr;
}



function editItemForRefugee(requester_id,r_id){
     // The callback function will need the following information : 
    document.getElementById('query-results').setAttribute('refresh_rid_after_edit', r_id); // request. 
    document.getElementById('query-results').setAttribute('refresh_requester_id_after_edit', requester_id); // 
    document.getElementById('query-results').setAttribute('refresh_producer_id_after_edit', ''); // 
    document.getElementById('query-results').setAttribute('refresh-after-modal-edit', 'refreshItemsDetailPage');
    editItemDetails(requester_id,r_id,'','refreshItemsDetailPage')
 }


//
// Inputs: None. 
// Attributes:   urlToUse is set to the URL to send the collected data to. 
//
function saveModalPerson(rcallback) { 
    // Collect names for the modal person...
  var personModal = document.getElementById('personModal')

  person_id = personModal.querySelector('#modalPerson_person_id').value;

  pdata= {
      "person_id": personModal.querySelector('#modalPerson_person_id').value ,
      "person_title": null,
      "person_type": personModal.getAttribute('typeOfPerson'),
      "person_djangoid": null,
      "person_firstname": personModal.querySelector('#modalPerson_firstname').value, 
      "person_middlename": null,
      "person_lastname": personModal.querySelector('#modalPerson_lastname').value,
      "person_suffix": null,
      "person_address1": personModal.querySelector('#modalPerson_address1').value,
      "person_address2": null,
      "person_city": personModal.querySelector('#modalPerson_city').value,
      "person_state":personModal.querySelector('#modalPerson_state').value ,
      "person_zip": personModal.querySelector('#modalPerson_zip').value ,
      "person_origincountry": null,
      "person_homephone": personModal.querySelector('#modalPerson_homephone').value,
      "person_workphone": null,
      "person_cellphone": personModal.querySelector('#modalPerson_cellphone').value,
      "person_email": personModal.querySelector('#modalPerson_email').value,
      "person_workemail": null,
      "person_gender": "1",
      "person_dob": null,
  }

  url = personModal.getAttribute('urlToUse')
  console.log("I will save to " + url + " this data " + JSON.stringify(pdata))
  how = "PUT"
  if (person_id == '') { 
    how = "POST"
    }
  sendJSON(url,pdata,how,rcallback);
}

function createOnboardRequests(requester_id) {


  
  var result = confirm("Are you sure you want to create these requests for this user?");

  console.log("RESULT-", result)

      if (result === true ) {
      var url = global_createOnboardRequests.replace('61',requester_id);

      console.log(url) ;
      readJSON(url,function(err, data) {
          if (err != null) {
            console.error(err);
          } else { 
            console.log(data);
            getAllPeople('REQUESTER')
 
          }
      })
  }
  
}
//
// Collect names for the modal person...
//
function saveModalRequest(rcallback) { 
        var requestObject = document.getElementById('requestModal')

        req_id = requestObject.querySelector('#modalReq_req_id').value;

        pdata= {
            "req_id": requestObject.querySelector('#modalReq_req_id').value ,
            "req_requester": requestObject.querySelector('#modalReq_requester').value ,
            "req_item_type": requestObject.querySelector('#modalReq_item_type').value ,
            "req_status": requestObject.querySelector('#modalReq_status').value ,
            "req_assigned_to": parseInt( requestObject.querySelector('#modalReq_assigned_to').value ),
            "req_quantity": requestObject.querySelector('#modalReq_quantity').value ,
            "req_title": requestObject.querySelector('#modalReq_title').value ,
            "req_description": requestObject.querySelector('#modalReq_description').value ,
            "req_notes": requestObject.querySelector('#modalReq_notes').value ,
            "req_time_taken": requestObject.querySelector('#modalReq_time_taken').value ,
            "req_neededbydate": requestObject.querySelector('#modalReq_neededbydate').value ,
            "req_filledbydate": requestObject.querySelector('#modalReq_filledbydate').value ,

        }
        // -----------------------------------------------------------------------------------------------------------------------
        // Important for preserving integrity of JSON API request packet. 
        // TODO -- set value of "" to null in json object for all FIELDS
        var fields = ['req_quantity', "req_item_type",  "req_status",  "req_neededbydate",  "req_filledbydate","req_time_taken" ]
        for ( var fi in fields ) {
          f = fields[fi]
          console.log(pdata[f], f)
          if (pdata[f] == "") {
            pdata[f] = null; 
            }
        }
  
  console.log("I will save first name here. for " + JSON.stringify(pdata))
  var url = global_requiredItemDetail.replace('22',req_id);
  var url1 = global_getAllRequestsByRequester.replace('61',p_id);
  how = "PUT"

  // -------------------- if this is a new request ----------------------------
  if (req_id == '') { 
    url = global_requiredItemList
    how = "POST"
    }
  console.log("Send to .." + document.getElementById('query-results').getAttribute('refreshItems') )


  var p_id = pdata['req_requester']; 
  var divname = '#details'
  //document.getElementById('query-results').setAttribute('refreshItems', true)

  document.getElementById('query-results').setAttribute('refreshItemsParms',  [p_id, url1, '#details' ]) 
  sendJSON(url,pdata,how,rcallback);
}

function removeOptions(selectElement) {
   if (selectElement == null) {
     return;
   }
   var i, L = selectElement.options.length - 1;
   for(i = L; i >= 0; i--) {
      selectElement.remove(i);
   }
}




// -------------------------------------------------------------------------------------------------
// r_id -- Requester ID
// req_id -- Request ID
// viewer - 'admin' shows all volunteers, other values disallow selecting producer. 
// rcallback  = null or a function pointer 
// -------------------------------------------------------------------------------------------------
function editItemDetails(r_id, req_id, viewer, rcallback ) { 
  // First get all the persons you can assign to, the types of items. and the status each item can take. 
  // then create the farging drop down lists and 
  // then show the actual dialog. 
  document.getElementById("query-results").setAttribute('json_request_index',req_id)
  document.getElementById("query-results").setAttribute('json_requester_id',r_id)  
  document.getElementById('query-results').setAttribute('refresh-after-modal-edit', rcallback);
  var url = global_getItemsForDialogBoxes.replace('0',req_id );

      readJSON(url,function(err, data) {
        if (err != null) {
          console.error(err);
        } else { 
          console.log(data);
          // Now create the drop down lists for three UI elements. 
          var requestObject = document.getElementById('requestModal')
          selectItem  = requestObject.querySelector('#modalReq_assigned_to')
          removeOptions(selectItem)
              // Producers who can be assigned a request. 
          for (var x=0;x<data.producers.length; x++ ) {
                  item = data.producers[x]
                  var xstr = `${item.person_firstname} ${item.person_lastname}`
                  var vstr = `${item.person_id}`
                  option = new Option(xstr,vstr); 
                  selectItem.append(option);
              }

          var hidethem = requestModal.querySelectorAll('.modal-admin-only')
          if (viewer == 'admin') {
           
            requestModal.querySelector('#modalReq_requester').readOnly    = false;    
            hidethem.forEach(useritem => {
              useritem.hidden = false;
            });

          } else { 
            hidethem.forEach(useritem => {
              useritem.hidden = true;
            });
            requestModal.querySelector('#modalReq_requester').readOnly    = true;    
            
          }
          // Producers who can be assigned a request. 
          // for (var x=0;x<data.producers.length; x++ ) {
          //   item = data.producers[x]
          //   var xstr = `${item.person_firstname} ${item.person_lastname}`
          //   var vstr = `${item.person_id}`
          //   option = new Option(xstr,vstr); 
          //   selectItem.append(option);
          // }
          selectItem  = requestObject.querySelector('#modalReq_item_type')
          removeOptions(selectItem)
          // Types of items from data base
          for (var x=0;x<data.itype.length; x++ ) {
            item = data.itype[x]
            var xstr = `${item.itm_Type} `
            var vstr = `${item.itm_id}`
            option = new Option(xstr,vstr);
            selectItem.append(option);
          }
          selectItem  = requestObject.querySelector('#modalReq_status')
          removeOptions(selectItem)
          // States of each request 
          for (var x=0;x<data.status.length; x++ ) {
            item = data.status[x]
            var xstr = `${item.itm_Status} `
            var vstr = `${item.itm_id}`
            option = new Option(xstr,vstr);
            selectItem.append(option);
          }
          // TODO: 
          // I should set up an object baseed on the person requesting 
          // and the item information as well. 
          var req_id = document.getElementById("query-results").getAttribute('json_request_index')
          var p_id   = document.getElementById("query-results").getAttribute('json_requester_id')
          // You CANNOT go by the index alone -- you have to match it. 
          if (req_id >= 0) {
            item = data.request
            console.log(item)
            requestModal.querySelector('#modalReq_req_id').value       = item.req_id; 
            requestModal.querySelector('#modalReq_requester').value    = item.req_requester_id;
            requestModal.querySelector('#modalReq_status').value      = item.req_status           
            requestModal.querySelector('#modalReq_item_type').value    = item.req_item_type; 
            requestModal.querySelector('#modalReq_assigned_to').value  = item.req_assigned_to; 
            requestModal.querySelector('#modalReq_quantity').value     = item.req_quantity; 
            requestModal.querySelector('#modalReq_title').value        = item.req_title; 
            requestModal.querySelector('#modalReq_description').value  = item.req_description; 
            requestModal.querySelector('#modalReq_notes').value  = item.req_notes; 
            requestModal.querySelector('#modalReq_time_taken').value     = item.req_time_taken; 
            requestModal.querySelector('#modalReq_neededbydate').value = item.req_neededbydate; 
            requestModal.querySelector('#modalReq_filledbydate').value = item.req_filledbydate;
          } else { 
            requestModal.querySelector('#modalReq_req_id').value       = ''; 
            requestModal.querySelector('#modalReq_requester').value    = p_id; 
          }
          $('#requestModal').modal('show');
        }
      })
}




// Shows a perosn whose id is shown. 
function showModalPerson(typeOfPerson, existing) {

    var personModal = document.getElementById('personModal')
    var modalTitle = personModal.querySelector('.modal-title')
    var modalBodyInput = personModal.querySelector('#modalPerson_person_id')
    var url;
    var person = existing; 

        if (existing == null) {
          url =  global_personsList;
          //personModal.querySelector('#modalPerson_person_id').setAttribute('readonly', false)
          // This is a dummy object. 
          person = {
                "person_id": '' ,
                "person_title": null,
                "person_type": typeOfPerson,
                "person_djangoid": null,
                "person_firstname": 'First', 
                "person_middlename": null,
                "person_lastname": "Last",
                "person_suffix": null,
                "person_address1": "",
                "person_address2": null,
                "person_city": personModal.querySelector('#modalPerson_city').value,
                "person_state":personModal.querySelector('#modalPerson_state').value ,
                "person_zip": personModal.querySelector('#modalPerson_zip').value ,
                "person_origincountry": null,
                "person_homephone": "12145551212",
                "person_workphone": null,
                "person_cellphone": "12145551212",
                "person_email": "abcd@def.com",
                "person_workemail": null,
                "person_gender": "1",
                "person_dob": null
          
              }

        } else { 

          url = global_personDetail.replace('22',existing.person_id); 
          // personModal.querySelector('#modalPerson_person_id').setAttribute('readonly', true)
          // This is an existing object. DO A FIELD BY FIELD TO SEE IF THE OBJECT MATCHES? 
          person = existing; 
          typeOfPerson = person.person_type; 
        }
          

      modalTitle.textContent = 'Edit ' + typeOfPerson
      personModal.setAttribute('typeOfPerson', typeOfPerson)
      personModal.querySelector('#modalPerson_person_id').value = person.person_id; 
      personModal.querySelector('#modalPerson_firstname').value = person.person_firstname; 
      personModal.querySelector('#modalPerson_lastname').value = person.person_lastname; 
      personModal.querySelector('#modalPerson_address1').value = person.person_address1; 
      personModal.querySelector('#modalPerson_city').value = person.person_city; 
      personModal.querySelector('#modalPerson_state').value = person.person_state; 
      personModal.querySelector('#modalPerson_zip').value = person.person_zip; 
      personModal.querySelector('#modalPerson_homephone').value = person.person_homephone; 
      personModal.querySelector('#modalPerson_cellphone').value = person.person_cellphone; 
      personModal.querySelector('#modalPerson_email').value = person.person_email; 
      console.log("Send to ", url)
      personModal.setAttribute('urlToUse', url)
      $('#personModal').modal('show');

}


