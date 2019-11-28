# -*- test-case-name: dreamuploader.test.test_vmsdata -*-

import attr
import typing
from base64 import b64decode
from datetime import datetime
from io import BytesIO
from struct import Struct
from urllib.parse import parse_qs

# Hey Sega, uhhhh, what the heck is this about?
DREAMCAST_BASE64_TRANSLATION = bytes.maketrans(
    b'AZOLYNdnETmP6ci3Sze9IyXBhDgfQq7l5batM4rpKJj8CusxRF+k2V0wUGo1vWH/=',
    b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='
)

VMI_CHECKSUM_FORMAT = Struct('<L')

VMI_CHECKSUM_BASE = VMI_CHECKSUM_FORMAT.unpack(b'SEGA')[0]

VMI_FORMAT = Struct('<L32s32sHBBBBBBBBH8s12sHHL')

@attr.s(auto_attribs=True)
class VMSData:
    """
    A representation of Dreamcast Visual Memory System data,
    including both the raw file and file-system metadata.
    """

    # Metadata for VMI sidecar file
    filename: str = None
    filesize: int = None
    timestamp: datetime = None
    version_minor: int = 0
    version_major: int = 0
    file_number: int = 1
    protected: bool = False
    game_data: bool = False

    # Raw Visual Memory file data
    vms: bytes = None

    # Default description/copyright text
    description: str = 'Dreamuploader for Python'
    copyright: str = 'Made with <3 in 2019 by @ticky'

    @classmethod
    def from_post_bytes(cls, inbytes):

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

        filename = metadata[b'filename'][0].decode()

        filesize = int(metadata[b'fs'][0])

        blocksize = int(metadata[b'bl'][0])

        timestamp = datetime.strptime(metadata[b'tm'][0].decode(), '%Y%m%d%H%M%S%w')

        # TODO: figure out what `tp`, `fl` and `of` are

        body = bytes.read()

        vms = b64decode(body.translate(DREAMCAST_BASE64_TRANSLATION))
        bytes.close()

        return cls(
            filename=filename,
            filesize=filesize,
            timestamp=timestamp,
            vms=vms
        )

    @classmethod
    def from_vmi(cls, vmi):

        (
            checksum,
            description, copyright,
            year, month, day, hour, minute, second, weekday,
            version_minor,
            version_major,
            file_number,
            vmsname,
            filename,
            mode,
            _,
            filesize
        ) = VMI_FORMAT.unpack(vmi)

        description = description.decode()
        copyright = copyright.decode()

        timestamp = datetime(year, month, day, hour, minute, second)

        vmsname = vmsname.decode()
        filename = filename.decode()

        protected = (mode << 0) == 1
        game_data = (mode << 1) == 1

        return cls(
            filename=filename,
            filesize=filesize,
            timestamp=timestamp,
            version_minor=version_minor,
            version_major=version_major,
            file_number=file_number,
            protected=protected,
            game_data=game_data,
            description=description,
            copyright=copyright
        )

    def to_vmi(self, vmsname):

        return VMI_FORMAT.pack(
            # Checksum header
            VMI_CHECKSUM_BASE & VMI_CHECKSUM_FORMAT.unpack(vmsname[0:4].encode())[0],

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

            # Minor version
            0,

            # Major version
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
