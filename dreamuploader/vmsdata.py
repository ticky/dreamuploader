# -*- test-case-name: dreamuploader.test.test_vmsdata -*-

import attr
from base64 import b64decode
from datetime import datetime
from io import BytesIO
import struct
from urllib.parse import parse_qs

# Hey Sega, uhhhh, what the heck is this about?
DREAMCAST_BASE64_TRANSLATION = bytes.maketrans(
    b'AZOLYNdnETmP6ci3Sze9IyXBhDgfQq7l5batM4rpKJj8CusxRF+k2V0wUGo1vWH/=',
    b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='
)

VMI_CHECKSUM_BASE = struct.unpack('<L', b'SEGA')[0]

VMI_FORMAT = '<L32s32sHBBBBBBHH8s12sHHL'

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

    # Default description/copyright text
    description = 'Dreamuploader for Python'
    copyright = 'Made with <3 in 2019 by @ticky'

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
        self.tp = int(tp[0])

        fl = metadata[b'fl']
        self.fl = int(fl[0])

        of = metadata[b'of']
        self.of = int(of[0])

        timestamp = metadata[b'tm']
        self.timestamp = datetime.strptime(timestamp[0].decode(), '%Y%m%d%H%M%S%w')

        body = bytes.read()

        self.vms = b64decode(body.translate(DREAMCAST_BASE64_TRANSLATION))
        bytes.close()

    def to_vmi(self, vmsname):

        return struct.pack(
            VMI_FORMAT,

            # Checksum header
            VMI_CHECKSUM_BASE & struct.unpack('<L', self.filename[0:4].encode())[0],

            # VMI file description/copyright
            self.description.encode(),
            self.copyright.encode(),

            # Date
            self.timestamp.year,
            self.timestamp.month,
            self.timestamp.day,
            self.timestamp.hour,
            self.timestamp.minute,
            self.timestamp.second,
            self.timestamp.weekday() + 1,

            # VMI format version
            0,

            # File number
            1,

            # Name of partner VMS file
            vmsname.encode(),

            # Filename when transferred to VMU
            self.filename.encode(),

            # File mode bitfield
            0, # TODO: Make this do the correct thing

            # Unused(?)
            0,

            # VMS File size in bytes
            self.filesize
        )

    # @classmethod
    # def from_path(cls, path):