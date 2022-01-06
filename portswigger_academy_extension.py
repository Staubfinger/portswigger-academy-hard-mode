try:
    from burp import IBurpExtender, IHttpListener
except ImportError as e :
    print("Failed to load dependencies. This issue may be caused by using the unstable Jython 2.7 beta.", e)

BURP_ACADEMY_DIV = '<div id="academyLabHeader">'
BURP_ACADEMY_HOST = ".web-security-academy.net"
CONTENT_LENGTH = "Content-Length"
CRLF = "\r\n"

class BurpExtender(IBurpExtender, IHttpListener):
    helpers = None
    callbacks = None

    def registerExtenderCallbacks(self, this_callbacks):

        self.callbacks = this_callbacks
        self.helpers = self.callbacks.getHelpers()

        self.callbacks.setExtensionName("PortSwigger Academy Hard-Mode")
        self.callbacks.registerHttpListener(self)

    def processHttpMessage(self, toolFlag, messageIsRequest, messageInfo):
        if not messageIsRequest:
            self.processResponse(messageInfo)

    def processResponse(self, httpRequestResponse):
        origReqBytes = httpRequestResponse.getRequest()
        origRespBytes = httpRequestResponse.getResponse()

        # Check if we're intercepting a response to a request to the web-academy AND
        # if its text/html attempt to transform the spoiler header for the extension to modify
        if(BURP_ACADEMY_HOST in httpRequestResponse.getHttpService().getHost()):    
            if(self.checkContentType('HTML', origRespBytes)):
                httpRequestResponse.setResponse(self.transformAcademyHTML(origRespBytes))   



    def transformfirstHTMLTag(self, tag, mode, content):
        START = '<{}'.format(tag) # so dirty
        END = '</{}>'.format(tag) 

        start = self.helpers.indexOf(content, self.helpers.stringToBytes(START), False, 0, len(content))
        end = self.helpers.indexOf(content, self.helpers.stringToBytes(END), False, 0, len(content))

        encode = "<!-- HARD-MODE: {} -->"
        # to put this in an html comment is kinda shitty, could use a div w/display:none, id=bla which is more easily accessible via javascript 

        # sadly we use python 2.x here so no new fancy python3.10 `match mode` code.
        if(mode == 'remove'):
            return self.helpers.bytesToString(content[:start]) + START + '>' + "PortSwigger Academy Hard-Mode" + END + self.helpers.bytesToString(content[end+len(END):]) 
        elif(mode == 'encode'):
            return self.helpers.bytesToString(content[:start]) + encode.format(self.helpers.base64Encode(content[start:end + len(END)])) + self.helpers.bytesToString(content[end+len(END):]) 

    # Take the Header and base64 encode it, so that the extension can decode it and display it if necessary - i.e for hints needed to solve the chall
    # base64 has a flaw, since if one observes the string one could potentially learn the patterns by heart for the different categories and spoil oneself again, but good enough for now.
    def transformAcademyHTML(self, responseBytes):
        # first of all make sure we potentially have hints in the response
        if (self.helpers.bytesToString(responseBytes).find(BURP_ACADEMY_DIV) == -1) :
            return responseBytes

        bodyOffset = self.helpers.analyzeResponse(responseBytes).getBodyOffset() 
        oldHeaders = self.helpers.analyzeResponse(responseBytes).getHeaders()
        oldResponseBody = responseBytes[bodyOffset:]

        newResponseBody = self.transformfirstHTMLTag('section', 'encode', oldResponseBody)
        newResponseBody = self.transformfirstHTMLTag('title', 'remove', newResponseBody)
        
        
        # this should also take care of the CL. Unclear what happens with HTTP/2 requests.  
        newResponse = self.helpers.buildHttpMessage(oldHeaders, newResponseBody)

        return newResponse
    
    def checkContentType(self, cntnt_type, response):
        return self.helpers.analyzeResponse(response).getStatedMimeType().startswith(cntnt_type)

    