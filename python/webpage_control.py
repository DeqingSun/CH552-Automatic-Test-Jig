import http.server
import socketserver
import urllib.parse
import time

from sketchTestCode.ch559_jig_code import CH559_jig

PORT = 8000

web_response_dict = {}
web_response_html = ["/"]

class GetHandler(http.server.SimpleHTTPRequestHandler):
    
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        if parsed_path.path in web_response_dict:
            resp_content = web_response_dict[parsed_path.path]
            self.protocol_version='HTTP/1.1'
            self.send_response(200, 'OK')
            if (parsed_path.path in web_response_html):
                self.send_header('Content-type', 'text/html')
            else:
                self.send_header('Content-type', 'text/plain')
            self.end_headers()
            if isinstance(resp_content, str):
                self.wfile.write(bytes(resp_content, 'UTF-8'))
            elif callable(resp_content):
                query_components = urllib.parse.parse_qs(parsed_path.query)
                function_resp = resp_content(query_components)
                if (type(function_resp) == str):
                    self.wfile.write(bytes(function_resp, 'UTF-8'))
                else:
                    self.wfile.write(bytes("call "+resp_content.__name__, 'UTF-8'))
            else:
                self.wfile.write(bytes("unknown ", 'UTF-8'))
        else:
            #logging.error(self.headers)
            http.server.SimpleHTTPRequestHandler.do_GET(self)

def root_page_handler(parameters):
    with open("webpage_template.html", "r") as f:
        webpage_template = f.read()
    return webpage_template

def ch559_init_handler(parameters):
    return str(ch559_jig.initailize(wait_for_input_time=1))

def ch559_connect_pins_handler(parameters):
    pin_x = int(parameters["x"][0])
    pin_y = int(parameters["y"][0])
    conn = int(parameters["conn"][0])
    if conn>0:
        return str(ch559_jig.connect_pins(pin_x, pin_y))
    else:
        return str(ch559_jig.disconnect_pins(pin_x, pin_y))

web_response_dict["/"]=root_page_handler
web_response_dict["/ch559_init"]=ch559_init_handler      
web_response_dict["/ch559_connect_pins"]=ch559_connect_pins_handler

ch559_jig = CH559_jig()
ch559_jig.connect()

Handler = GetHandler
socketserver.TCPServer.allow_reuse_address = True   #debugging, avoid port in use shortly after restart script
httpd = socketserver.TCPServer(("", PORT), Handler)
httpd.serve_forever()
