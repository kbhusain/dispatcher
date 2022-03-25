  // Network related actions. Not related to django,.






function readJSON(url,callback) { 
    let result = document.querySelector('.result');
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
          createItemCards(pid, divname,data['data'], {'showUnassign': true, 'showAssign':false}) ;
        }
      })
}


