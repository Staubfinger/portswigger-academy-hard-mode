
div_className_solved = "is-solved";
div_className_Notsolved = "is-notsolved";
div_lab_class = "cta"

labs = []

function getFirstLink(div){
    var children = Array.from(div.childNodes);
    var child;

    for(child in children){
        if(children[child].tagName == 'A'){
            console.log(new URL(children[child].href).pathname.split('/')[2])
            return children[child].href
        }
    }
    // what is here implicitly being returned if non of the childNodes is <a>? is it the result from the first assignment? null? undefined? 
}

// doing the DOM-Parsing here, just for being cautious and i guess XSS in popup.js is less worse than in background.js?

function startLab(data){
    html = data.html
    var mydocument = new DOMParser().parseFromString(html, 'text/html')
    div = mydocument.getElementsByClassName(div_lab_class)[0]
    url = div.firstElementChild.href
    let meh = browser.runtime.sendMessage({type: 'openLab', url: url}) // does the actual new open tab
    meh.then(() => {browser.browserAction.setPopup({popup: 'lab.html'}); window.close()})
    // TODO FIX for the above: Promise rejected after context unloaded: Actor 'Conduits' destroyed before query 'RuntimeMessage' was resolved
}

function handleLabs(data){
    console.log("Handling Labs", data)
    html = data.html
     // parseHTML for unsolved labs, compile a list 
     var mydocument = new DOMParser().parseFromString(html, 'text/html')
     divs = mydocument.getElementsByClassName(div_className_Notsolved) // change this for testing purposes to solved - if you dont want to spoil yourself
     for (const div of divs) {
         labs.push(getFirstLink(div))    
     }
     // pick a random lab
     next_lab = labs[Math.floor((Math.random() * labs.length))] // works since random return value in [0,1)

     var page = browser.runtime.sendMessage({
        type: 'getLab',
        url: next_lab
    })
    page.then(startLab, handleError)
}

async function handleError(err){
    await console.log(err)
    console.log(err)
    console.log(err)
}

function move(){
    browser.browserAction.setPopup({popup: 'lab.html'})
    window.close() 
}

function listenForClicks() {
    document.addEventListener("click", (e) => {
  

      function create() {
        // ask background about html of all-labs
        var request = browser.runtime.sendMessage({
            type: 'labs' 
          });
        request.then(handleLabs, handleError);
     }

      if (e.target.classList.contains("lab")) {
        create()
      }
      if (e.target.classList.contains("move")) {
        move()
      }
    });
  }
  
listenForClicks()