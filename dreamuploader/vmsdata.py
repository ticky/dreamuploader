# -*- test-case-name: dreamuploader.test.test_vmsdata -*-

import attr
from base64 import b64decode
from datetime import datetime
from io import BytesIO
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
