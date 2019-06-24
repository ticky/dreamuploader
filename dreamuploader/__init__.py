# -*- test-case-name: dreamuploader.test -*-

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

############ TODO: Split this into a separate file bc this is no way to live ############

import attr
from base64 import b64decode
from datetime import datetime
from urllib.parse import parse_qs

# Hey Sega, uhhhh, what the heck is this about?
DREAMCAST_BASE64_TRANSLATION = bytes.maketrans(
    b'AZOLYNdnETmP6ci3Sze9IyXBhDgfQq7l5batM4rpKJj8CusxRF+k2V0wUGo1vWH/=',
    b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='
)

class VMSData:
    """
    A representation of Dreamcast Visual Memory System data,
    including both the raw file and file-system metadata.
    """

    # Raw Visual Memory file data
    vms = None

    # Metadata for VMI sidecar file
    filename = None
    filesize = None
    blocksize = None
    tp = None # TODO: oWo What is this? 🤔
    fl = None # TODO: oWo What is this? 🤔
    of = None # TODO: oWo What is this? 🤔
    timestamp = None

    def __init__(self, inbytes):

        bytes = BytesIO(inbytes)
        header = BytesIO()

        nextLine = bytes.readline()

        while nextLine:
            strippedLine = nextLine.strip()

            if strippedLine is not b'':
                header.write(strippedLine)
            else:
                break

            nextLine = bytes.readline()

        header.seek(0)
        metadata = parse_qs(header.read())
        header.close()

        filename = metadata[b'filename']
        self.filename = filename[0].decode()

        filesize = metadata[b'fs']
        self.filesize = int(filesize[0])

        blocksize = metadata[b'bl']
        self.blocksize = int(blocksize[0])

        tp = metadata[b'tp']
        self.tp = tp[0]

        fl = metadata[b'fl']
        self.fl = fl[0]

        of = metadata[b'of']
        self.of = of[0]

        timestamp = metadata[b'tm']
        self.timestamp = datetime.strptime(timestamp[0].decode(), '%Y%m%d%H%M%S%w')

        body = bytes.read()

        self.vms = b64decode(body.translate(DREAMCAST_BASE64_TRANSLATION))
        bytes.close()

    # @classmethod
    # def from_path(cls, path):

