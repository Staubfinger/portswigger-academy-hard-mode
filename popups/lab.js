/// gen HTML for lab.html
/**

categories = ['sql-injection','cross-site-scripting','csrf','clickjacking','cors',''dom-based,'xxe','ssrf','request-smuggling','os-command-injection','server-side-template-injection','file-path-traversal','access-control','authentication','websockets','web-cache-poisoning','deserialization','information-disclosure','logic-flaws','host-header','oauth','file-upload']

HTMLString = ''

function getName(string){
    // want to do meow-catz into Meow Catz
    string = string.replace(/-([a-z])/g, function (g) { return " " + g[1].toUpperCase(); });
    return string[0].toUpperCase() + string.substring(1)
}

categories.forEach(curr => {
    Options_HTML = `<option value="${curr}">${getName(curr)}</option>`
    HTMLString += Options_HTML
});

console.log(HTMLString)
 
*/

function listenForClicks() {
    document.addEventListener("click", (e) => {
  

    function submithint() {
        console.log(`Submitting Hint request with ${document.getElementById("cat").value}`)
        browser.runtime.sendMessage({
            type: 'hint',
            hint: document.getElementById("cat").value
          });
     }
  
      function reset() {
        browser.browserAction.setPopup({popup: browser.runtime.getURL('popups/popup.html')})
        window.close()
      }
 
      if (e.target.classList.contains("hint")) {
        submithint()
      }

        else if (e.target.classList.contains("reset")) {
        reset()
 }

    });
  }
  
listenForClicks()
