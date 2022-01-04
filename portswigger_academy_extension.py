try:
    from burp import IBurpExtender, IHttpListener
except ImportError as e :
    print("Failed to load dependencies. This issue may be caused by using the unstable Jython 2.7 beta.", e)

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
        # to put this in an html comment is kinda shitty, could use a div w/display:none which is more easily accessible via javascript 

        # sadly we use python 2.x here so no new fancy python3.10 `match mode` code.
        if(mode == 'remove'):
            return self.helpers.bytesToString(content[:start]) + START + '>' + "PortSwigger Academy Hard-Mode" + END + self.helpers.bytesToString(content[end+len(END):]) 
        elif(mode == 'encode'):
            return self.helpers.bytesToString(content[:start]) + encode.format(self.helpers.base64Encode(content[start:end + len(END)])) + self.helpers.bytesToString(content[end+len(END):]) 

    # Take the Header and base64 encode it, so that the extension can decode it and display it if necessary - i.e for hints needed to solve the chall
    # base64 has a flaw, since if one observes the string one could potentially learn the patterns by heart for the different categories and spoil oneself again, but good enough for now.
    def transformAcademyHTML(self, responseBytes):
        # i guess some more checking is needed for html responses that do not contain the lab header    
        newResponse = self.transformfirstHTMLTag('section', 'encode', responseBytes)
        newResponse = self.transformfirstHTMLTag('title', 'remove', newResponse)
        
        # fixing content length :@ - kinda weird no native functions are available for this. needs _really_ ugly hacking. 
        # note: the functions which automatically update the CL do not work here, seemingly, as we're editing raw HTML and not body post variables 
        
        # calc new content-len
        body_offset = self.helpers.analyzeResponse(responseBytes).getBodyOffset() 
        new_CL = len(newResponse) - body_offset
        
        # get the index of the old content length header
        idx = self.helpers.indexOf(newResponse, self.helpers.stringToBytes(CONTENT_LENGTH), False , 0, len(newResponse))
        
        # get the end idx of the old header
        # pretty much the definiton of shit - pls giev self.helpers.updateCL(newcl=1337)  // the 15 is kinda arbitrary but should be fine
        end_idx = self.helpers.indexOf(newResponse, CRLF, False , idx, idx + len(CONTENT_LENGTH) + 15)      

        # forge new response with old header left out and replaced with new header with new CL
        newResponse = newResponse[:idx] + str(CONTENT_LENGTH) + str(": ") + str(new_CL) + CRLF + newResponse[end_idx + 2:]

        return newResponse
    
    def checkContentType(self, cntnt_type, response):
        return self.helpers.analyzeResponse(response).getStatedMimeType().startswith(cntnt_type)

    