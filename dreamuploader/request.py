# -*- test-case-name: dreamuploader.test.test_request -*-

from io import BytesIO
from twisted.web import server
from twisted.web.http import _parseHeader

MULTIPART_BOUNDARY_DELIMITER = b'--'

class DreamuploaderRequest(server.Request):
    """
    An HTTP request which has been pre-processed to
    handle the quirks of Sega Dreamcast browsers.
    """

    def requestReceived(self, command, path, version):
        ctype = self.requestHeaders.getRawHeaders(b'content-type')

        # if this request is sending multipart data
        if ctype is not None and ctype[0][:10] == b'multipart/':
            ctype = ctype[0]

            clength = self.requestHeaders.getRawHeaders(b'content-length')
            if clength is not None:
                clength = int(clength[0])

            contentType, contentTypeParameters = _parseHeader(ctype)

            boundary = contentTypeParameters['boundary']
            compliantBoundary = MULTIPART_BOUNDARY_DELIMITER + boundary

            replacementsMade = 0
            originalOk = False
            newContent = BytesIO()
            self.content.seek(0)

            nextLine = self.content.readline()

            while nextLine and not originalOk:
                strippedLine = nextLine.strip()

                if strippedLine == boundary or strippedLine == boundary + MULTIPART_BOUNDARY_DELIMITER:
                    # the incoming payload is non-compliant
                    # in the way Dream Passport is; correct it
                    replacementsMade += 1
                    newContent.write(MULTIPART_BOUNDARY_DELIMITER + nextLine)

                elif strippedLine == compliantBoundary:
                    # the incoming payload is compliant,
                    # (this likely means no lines will be
                    # wrong and we should bail early!)
                    originalOk = True
                    newContent.close()

                else:
                    # this isn't a line we can make judgements about
                    newContent.write(nextLine)

                nextLine = self.content.readline()

            if replacementsMade > 0:
                self.content.close()
                self.content = newContent
                self.requestHeaders.setRawHeaders(b'content-length', [str(clength + replacementsMade * 2)])

        # finally, hand it on back to the original Request class
        super(DreamuploaderRequest, self).requestReceived(command, path, version)
