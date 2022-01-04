function handleLogin(data) {
    console.log(data)
    if(data.loggedIn){
        // do something that only logged in users can do
        window.location.href="default.html";
    }else{
        // prompt user to login
        window.location.href="login.html";
    }
}
  
function handleError(error) {
    console.log(`Error: ${error}`);
}

async function checkLoginStatus(){
        var request = browser.runtime.sendMessage({
          type: 'login' 
        });
        request.then(handleLogin, handleError);
}

// maybe don't spam the UI button all that much, as itll generate a request each time. 
checkLoginStatus()

