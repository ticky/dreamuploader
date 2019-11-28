import unittest
from datetime import datetime
import os

from dreamuploader.vmsdata import VMSData

dir_path = os.path.dirname(os.path.realpath(__file__))

def read_fixture(name):
    return open(os.path.join(dir_path, 'fixtures', name), 'rb').read()

CAPVSSNK_PLANETWEB = read_fixture('CAPVSSNK_SYS-Planetweb.txt')

CAPVSSNK_DREAMPASSPORT = read_fixture('CAPVSSNK_SYS-DreamPassport.txt')
CAPVSSNK_VMS = read_fixture('CAPVSSNK.VMS')
CAPVSSNK_VMI = read_fixture('CAPVSSNK.VMI')

PYOFEVER_DREAMPASSPORT = read_fixture('PUYOFEVERSYS-DreamPassport.txt')
PYOFEVER_VMS = read_fixture('PYOFEVER.VMS')
PYOFEVER_VMI = read_fixture('PYOFEVER.VMI')

BS_BM_M_VMI = read_fixture('BS_BM_M_.VMI')

class VMSDataTests(unittest.TestCase):

    def test_planetwebFormatCAPVSSNKPOSTInput(self):

        # Planetweb uses Windows-style line endings
        parsed = VMSData.from_post_bytes(CAPVSSNK_PLANETWEB)
        self.assertEqual(parsed.vms, CAPVSSNK_VMS)
        self.assertEqual(parsed.filename, 'CAPVSSNK_SYS')
        self.assertEqual(parsed.filesize, 4608)
        self.assertEqual(parsed.timestamp, datetime.fromisoformat('2019-06-22T22:51:40'))
        self.assertEqual(parsed.version_minor, 0)
        self.assertEqual(parsed.version_major, 0)
        self.assertEqual(parsed.file_number, 1)
        self.assertEqual(parsed.protected, False)
        self.assertEqual(parsed.game_data, False)
        self.assertEqual(parsed.to_vmi('CAPVSSNK'), CAPVSSNK_VMI)

    def test_dreamPassportFormatCAPVSSNKPOSTInput(self):

        # Dream Passport uses Unix-style line endings
        parsed = VMSData.from_post_bytes(CAPVSSNK_DREAMPASSPORT)
        self.assertEqual(parsed.vms, CAPVSSNK_VMS)
        self.assertEqual(parsed.filename, 'CAPVSSNK_SYS')
        self.assertEqual(parsed.filesize, 4608)
        self.assertEqual(parsed.timestamp, datetime.fromisoformat('2019-06-22T22:51:40'))
        self.assertEqual(parsed.version_minor, 0)
        self.assertEqual(parsed.version_major, 0)
        self.assertEqual(parsed.file_number, 1)
        self.assertEqual(parsed.protected, False)
        self.assertEqual(parsed.game_data, False)
        self.assertEqual(parsed.to_vmi('CAPVSSNK'), CAPVSSNK_VMI)

    def test_dreamPassportFormatPUYOFEVERSYSPOSTInput(self):

        parsed = VMSData.from_post_bytes(PYOFEVER_DREAMPASSPORT)
        self.assertEqual(parsed.vms, PYOFEVER_VMS)
        self.assertEqual(parsed.filename, 'PUYOFEVERSYS')
        self.assertEqual(parsed.filesize, 2048)
        self.assertEqual(parsed.timestamp, datetime.fromisoformat('2005-08-28T23:27:24'))
        self.assertEqual(parsed.version_minor, 0)
        self.assertEqual(parsed.version_major, 0)
        self.assertEqual(parsed.file_number, 1)
        self.assertEqual(parsed.protected, False)
        self.assertEqual(parsed.game_data, False)
        self.assertEqual(parsed.to_vmi('PYOFEVER'), PYOFEVER_VMI)

    def test_fromVMICAPVSSNK(self):

        parsed = VMSData.from_vmi(CAPVSSNK_VMI)
        self.assertEqual(parsed.vms, None)
        self.assertEqual(parsed.filename, 'CAPVSSNK_SYS')
        self.assertEqual(parsed.filesize, 4608)
        self.assertEqual(parsed.timestamp, datetime.fromisoformat('2019-06-22T22:51:40'))
        self.assertEqual(parsed.version_minor, 0)
        self.assertEqual(parsed.version_major, 0)
        self.assertEqual(parsed.file_number, 1)
        self.assertEqual(parsed.protected, False)
        self.assertEqual(parsed.game_data, False)
        self.assertEqual(parsed.to_vmi('CAPVSSNK'), CAPVSSNK_VMI)

    def test_fromVMIBS_BM_M(self):

        parsed = VMSData.from_vmi(BS_BM_M_VMI)
        self.assertEqual(parsed.vms, None)
        self.assertEqual(parsed.filename, 'DREAMKEY.S90')
        self.assertEqual(parsed.filesize, 5632)
        self.assertEqual(parsed.timestamp, datetime.fromisoformat('2003-09-12T10:50:58'))
        self.assertEqual(parsed.version_minor, 1)
        self.assertEqual(parsed.version_major, 1)
        self.assertEqual(parsed.file_number, 1)
        self.assertEqual(parsed.protected, False)
        self.assertEqual(parsed.game_data, False)
        self.assertEqual(parsed.to_vmi('BS_BM_M_'), BS_BM_M_VMI)
