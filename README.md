# Superseeded by: 
PortSwigger has introduced the [Mystery Lab Challenge](https://portswigger.net/blog/introducing-the-mystery-lab-challenge) which is a more or less one-by-one resemblence of what this projects aims to do. As theirs of course has lots more eye candy and does not need to overcome certain obstacles via browser+burp extensions its *HIGHLY* recommended to use that feature instead. Leaving the rest in here for educational purposes and curious minds.


## PortSwigger Academy Hard-Mode
This Browser + Burp Suite Extension aim to make the PortSwigger Academy more challenging. This is designed for people interested in not only practicing their exploitation technique but also bug finding abilities. Usually, one has to open a lab by hand which reveal what this lab is about and hints away where exactly the bug is. With this extension combo, a random lab which is not solved yet is being opened, and the lab header html and the title of the page, both of which include spoilers, are being removed or ""obfuscated"". (Such that it can be displayed at a later point in time). 

This whole extension is written just for fun and education purposes - and was written on a pure "Works for me" basis. Best read the code if you want to know whats going on - its really not that much :D 

## How To:
1. Clone the Repo
   -  `about:debugging` in FF - load extension by manifest
   -  in `Burp Suite` load the `portswigger_academy_extension.py` as new extension
      - This needs a configured Pyhton Environment. Download the Standalone jython binary [here](https://www.jython.org/download.html)

1. Open a new Lab via the extensions popup
2. ???
3. Profit

At some point while solving a lab you will get an idea of what this lab is about and know the general category. If you're still stuck then, open the Popup again and guess the right category which will reveal what this lab is about and might have additional information needed to solve the lab. 

## Debugging:
`CRTL + SHIFT + J` opens the browser console in ff, there top right settings menu tick the top most option (`Show Content Messages` in en) to see extension console.logs().

## Limitations:
- Some Labs have information in the hint HTML which is needed in order to solve the lab. For instance XSS w/Exploit Server, or Authentication with credentials.
  - Try to solve the lab as far as possible until feeling properly stuck and know that the final bits needed to solve the lab are in the HTML, i.e a url to an exploit server.
  - If there is a Login, try the "default" creds: `wiener/peter` and try to attack the account `carlos`.
-  Lab Category and title are reflected in the redirect URI while loading a new lab, no straight forward fix.
   - Workarround: Do not peek at the URL while opening a new lab
   - a fix might be a reverse proxy "service" to hide the URL 

## Improvments:
-  HTML/CSS for the popup is ugly, improve yourself if you care
-  Currently, when a lab timeouts there is no way to re-open the same lab. Could save the URL and add functionality to re-open the last lab.
   - a workarround for this is to guess the category and use the included back-link to get back to portswigger and open the lab manually
-  Icon is still default from the [FF examples](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/Your_first_WebExtension) - could change to something more portswigger themed

## Known BUGS:
- Some labs, for instance the insecure file upload ones, require the solution to be submitted via a form in the lab header. This form is implemented in javascript via an <script> which does not get executed upon inserting the HTML in background.js into the page, since the DOM is already loaded. 
   - Is a possible workaround to detect scripts and fetch/eval the code? Sounds horrible.  
   - temp workarround is to get the js yourself and paste it into the console ????
