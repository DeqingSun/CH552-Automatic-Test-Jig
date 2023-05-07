import http.server
import socketserver
import urllib.parse


PORT = 8000

webRespDict = {}

class GetHandler(http.server.SimpleHTTPRequestHandler):
    
    def do_GET(self):
        parsedPath = urllib.parse.urlparse(self.path)
        if parsedPath.path in webRespDict:
            respContent = webRespDict[parsedPath.path]
            self.protocol_version='HTTP/1.1'
            self.send_response(200, 'OK')
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            if isinstance(respContent, str):
                self.wfile.write(bytes(respContent, 'UTF-8'))
            elif callable(respContent):
                query_components = urllib.parse.parse_qs(parsedPath.query)
                functionResp = respContent(query_components)
                if (type(functionResp) == str):
                    self.wfile.write(bytes(functionResp, 'UTF-8'))
                else:
                    self.wfile.write(bytes("call "+respContent.__name__, 'UTF-8'))
            else:
                self.wfile.write(bytes("unknown ", 'UTF-8'))
        else:
            #logging.error(self.headers)
            http.server.SimpleHTTPRequestHandler.do_GET(self)





webRespDict["/version"]=("Dobot device version: %d.%d.%d" % (device.majorVersion, device.minorVersion, device.revision))


# webRespDict["/jog"]=jogMachine
# webRespDict["/emotor"]=moveEMotor
# webRespDict["/pose"]=getPose
# webRespDict["/home"]=home
# webRespDict["/moveinc"]=moveInc
# webRespDict["/test"]=test

    




Handler = GetHandler
socketserver.TCPServer.allow_reuse_address = True   #debugging, avoid port in use shortly after restart script
httpd = socketserver.TCPServer(("", PORT), Handler)
httpd.serve_forever()

