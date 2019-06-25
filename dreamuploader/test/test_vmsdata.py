import unittest
from datetime import datetime
import os

from dreamuploader.vmsdata import VMSData

dir_path = os.path.dirname(os.path.realpath(__file__))

def read_fixture(name):
    return open(os.path.join(dir_path, 'fixtures', name), 'rb').read()

CAPVSSNK_PLANETWEB = read_fixture('CAPVSSNK_SYS-Planetweb.txt')
CAPVSSNK_DREAMPASSPORT = read_fixture('CAPVSSNK_SYS-DreamPassport.txt')
CAPVSSNK_VMS = read_fixture('CAPVSSNK_SYS.VMS')
CAPVSSNK_VMI = read_fixture('CAPVSSNK.VMI')

class VMSDataTests(unittest.TestCase):

    def test_planetwebFormatInput(self):

        # Planetweb uses Windows-style line endings
        parsed = VMSData(CAPVSSNK_PLANETWEB)
        self.assertEqual(parsed.vms, CAPVSSNK_VMS)
        self.assertEqual(parsed.filename, 'CAPVSSNK_SYS')
        self.assertEqual(parsed.filesize, 4608)
        self.assertEqual(parsed.blocksize, 9)
        self.assertEqual(parsed.timestamp, datetime.fromisoformat('2019-06-22T22:51:40'))
        self.assertEqual(parsed.to_vmi('CAPVSSNK'), CAPVSSNK_VMI)

    def test_dreamPassportFormatInput(self):

        # Dream Passport uses Unix-style line endings
        parsed = VMSData(CAPVSSNK_DREAMPASSPORT)
        self.assertEqual(parsed.vms, CAPVSSNK_VMS)
        self.assertEqual(parsed.filename, 'CAPVSSNK_SYS')
        self.assertEqual(parsed.filesize, 4608)
        self.assertEqual(parsed.blocksize, 9)
        self.assertEqual(parsed.timestamp, datetime.fromisoformat('2019-06-22T22:51:40'))
        self.assertEqual(parsed.to_vmi('CAPVSSNK'), CAPVSSNK_VMI)
