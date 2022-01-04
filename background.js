// get data from portswigger to populate popup.html
url_base = "https://portswigger.net"
url_login = url_base + "/users/youraccount"
url_labs = url_base + "/web-security/all-labs"

var current_lab_category = null
var current_hint_html = null
var current_lab_tab_id = null

async function handleMessage(request) {
    console.log(`Received: ${request.type}`);
    resp = {}
    switch (request.type) {
        case 'login':
            // fetch(url_login).then((data) => {return Promise.resolve({loggedIn: !data.redirected})})
            data = await fetch(url_login)
            console.log("LoggedIn: ", !data.redirected)
            resp = {'loggedIn': !data.redirected}
            break;
        case 'labs':
            res = await (await fetch(url_labs)).text()
            console.log("Sending data back", res)
            resp = {'html': res}
            break;
        case 'getLab':
            path = new URL(request.url).pathname 
            // sample URL https://portswigger.net/web-security/sql-injection/..
            current_lab_category = path.split('/')[2]

            data = await (await fetch(url_base + path)).text()
            resp = {'html': data}
            break;
        case 'openLab':
            url = new URL(request.url)
             // ok here is a another major flaw. We have to create a new tab with the URL, since fetch with a manual redirect does not allow seeing the redirect url, due to XS-Leaks.
            // Could be improved perhapds? For now i just rely on myself not peeking at the URL while creating a new Lab. Idea for improvement, open new tab on the portswigger academy, use Content Script to inject full-screen iFrame with the lab URL?   
            // https://github.com/whatwg/fetch/issues/763 thx XS-Leaks 
            var tab = await browser.tabs.create({url: url_base + url.pathname + url.search})             
            current_lab_tab_id = tab.id
            
            break;
        case 'hint':
            console.log("Current category:", current_lab_category)
            // could check if category is set - if not, some1 opend lab externally 

            if(request.hint == current_lab_category){ // could implement anti-spam counter
                console.log("Sending tab message")
                // await browser.tabs.sendMessage(current_lab_tab_id, {type: 'inject_header', html: current_hint_html})
                browser.tabs.executeScript(current_lab_tab_id, {code: `
                let here = document.getElementById('academyLabHeader')
                here.innerHTML = atob(document.getElementById('academyLabHeader').childNodes[1].data.substr(12).trim())    
                `})
                
                resp = {'hint': true}
            }else{
                resp = {'hint': false}
            }
            break;
    }
    return Promise.resolve(resp)
}

browser.runtime.onMessage.addListener(handleMessage);


