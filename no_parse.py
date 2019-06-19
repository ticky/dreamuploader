
import sys
import klein
from twisted.python import log
from twisted.web import server
from twisted.internet import reactor
from twisted.internet.endpoints import serverFromString

log.startLogging(sys.stdout)

class NonParsingRequest(server.Request):

    def requestReceived(self, command, path, version):
        self.content.seek(0,0)
        self.args = {}

        self.method, self.uri = command, path
        self.clientproto = version
        x = self.uri.split(b'?', 1)

        if len(x) == 1:
            self.path = self.uri
        else:
            self.path, argstring = x
            self.args = parse_qs(argstring, 1)

        # Argument processing
        args = self.args
        ctype = self.requestHeaders.getRawHeaders(b'content-type')
        clength = self.requestHeaders.getRawHeaders(b'content-length')
        if ctype is not None:
            ctype = ctype[0]

        if clength is not None:
            clength = clength[0]

        self.process()


app = klein.Klein()

@app.route("/",  methods=['POST'])
def post(request):
    print(request.content.getvalue())
    return request.content.getvalue()


site = server.Site(app.resource())
site.requestFactory = NonParsingRequest

endpoint = serverFromString(reactor, "tcp:8080")
endpoint.listen(site)

reactor.run()
