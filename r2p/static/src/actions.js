  // Network related actions. Not related to django,.

 

function readJSON(url,callback) { 
    let result = document.querySelector('.result');
    var csrftoken =  document.querySelector('[name=csrfmiddlewaretoken]').value
    let xhr = new XMLHttpRequest();
    console.log(url)
    xhr.open("GET", url, true);
    xhr.responseType = "json"
    // xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader('X-CSRFToken', csrftoken );

    xhr.onreadystatechange = function () {
                if (xhr.readyState === 4 && xhr.status === 200) {
                // Print received data from server
                   callback(null, xhr.response);
                }
            };

    xhr.send();
}

function sendJSON(url, json_data, how, refreshcallback){
  var csrftoken =  document.querySelector('[name=csrfmiddlewaretoken]').value
    
    let result = document.querySelector('#send_result');
    // let name = document.querySelector('#name');
    // let email = document.querySelector('#email');
      
    // Creating a XHR object
    let xhr = new XMLHttpRequest();
    

    // open a connection either PUT or POST
    xhr.open(how, url, true);

    // Set the request header i.e. which type of content you are sending
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader('X-CSRFToken', csrftoken );

    // Create a state change callback
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {

            // Print received data from server
            if (result != null ) {
              //result.innerHTML = this.responseText;
              console.log(this.responseText)

            }
            console.log("refesh callback is checked here ...")
            if (refreshcallback != null ) {
                console.log("refesh callback is there")
                refreshcallback(); 
            }                
        }
    };

    // Converting JSON data to string
    console.log(json_data)
    var data = JSON.stringify(json_data);
    // Sending data with the request
    console.log(data)
    xhr.send(data);
}

        
function showRequestdetailsForPerson(pid, url, divname) {
    console.log(pid,url, divname)
    readJSON(url,function(err, data) {
        if (err != null) {
          console.error(err);
        } else { 
          console.log(data);
          createItemCards(pid,divname,data['data'], {'showUnassign': true, 'showAssign':false , 'showDelete': true }) ;
        }
      })
}


function printDiv(divName) {
    var printContents = document.getElementById(divName).innerHTML;
    var originalContents = document.body.innerHTML;
    document.body.innerHTML = printContents;
    window.print();
    document.body.innerHTML = originalContents;
}

function printDiv(divID) {
    //Get the HTML of div
    var divElements = document.getElementById(divID).innerHTML;
    //Get the HTML of whole page
    var oldPage = document.body.innerHTML;

    //Reset the page's HTML with div's HTML only
    document.body.innerHTML = 
       "<html><head><title></title></head><body>" + 
              divElements + "</body>";

    //Print Page
    window.print();

    //Restore orignal HTML
    document.body.innerHTML = oldPage;
          
}


 
function printDiv(divId,
  title) {

  let mywindow = window.open('', 'PRINT', 'height=650,width=900,top=100,left=150');

  mywindow.document.write(`<html><head><title>${title}</title>`);
  mywindow.document.write('</head><body >');
  mywindow.document.write(document.getElementById(divId).innerHTML);
  mywindow.document.write('</body></html>');

  mywindow.document.close(); // necessary for IE >= 10
  mywindow.focus(); // necessary for IE >= 10*/

  mywindow.print();
  mywindow.close();

  return true;
}
/*
<p>don't print this to pdf</p>
<div id="pdf">
  <p>
    <font size="3" color="red">print this to pdf</font>
  </p>
</div>

<button onclick="printDiv('pdf','Title')">print div</button>

<button onclick="saveDiv('pdf','Title')">save div as pdf</button>
*/


