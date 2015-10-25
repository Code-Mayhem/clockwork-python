import SimpleHTTPServer
import SocketServer
import jsonpickle
import sys

port = 5000

if len(sys.argv) >= 1:
    port = int(sys.argv[1])

startsWithString = '/receive-sms?'

smsCache = []

def parse_valid_path(path):
    pathToTokenize = path[len(startsWithString):]
    tokenizedByParameters = pathToTokenize.split('&')
    smsObject = {}
    for token in tokenizedByParameters:
        keyValuePair = token.split("=",1)
        smsObject[keyValuePair[0]] = keyValuePair[1]
    smsCache.append(smsObject)

class MyRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        myPath = self.path
        if myPath.startswith(startsWithString):
            parse_valid_path(myPath)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            jsonResult = jsonpickle.encode(smsCache)
            self.wfile.write(jsonResult)
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write("fail")
        return

Handler = MyRequestHandler
server = SocketServer.TCPServer(('0.0.0.0', port), Handler)

server.serve_forever()
