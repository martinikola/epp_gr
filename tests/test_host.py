from unittest import TestCase
from epp_gr.EppClient import EppClient

class TestHost(TestCase):

    # host = "ns1.forth.gr"
    # host_available = False

    host = "ns.bizelia.gr"
    host_available = True

    def setUp(self):
        self.epp = EppClient()
        self.login_result = self.epp.login()

    def tearDown(self):
        self.epp.logout()

    def test_host_check(self):
        host_check = self.epp.host_check(self.host)
        assert host_check is self.host_available, self.epp.last_result_code

    def test_host_info(self):
        host_info = self.epp.host_info(self.host)
        if self.host_available:
            assert host_info['name'] == self.host, self.epp.last_result_code
        else:
            assert host_info is None, self.epp.last_result_code

    def test_host_create(self):
        host_info = {
            'name': {self.contact_id},
            'loc_name': 'ΝΕΚΤΑΡΙΟΣ ΑΡΑΚΑΣ',
            'loc_org': 'ΕΛΛΗΝΙΚΑ',
            'loc_street1': 'ΑΧΑΡΝΩΝ',
            'loc_street2': 'ΠΑΠΑΦΛΕΣΣΑ',
            'loc_street3': '',
            'loc_city': 'ΑΘΗΝΑ',
            'loc_sp': 'ΠΕΙΡΑΙΑΣ',
            'loc_pc': '12345',
            'loc_cc': 'gr',
            # το καταργησα, ειναι παιδεμα η υλοποιηση...
            # 'int_name': 'John Doe',
            # 'int_org': 'Example Organization',
            # 'int_street1': '789 International Blvd',
            # 'int_street2': 'Floor 10',
            # 'int_street3': 'Tower XYZ',
            # 'int_city': 'Global City',
            # 'int_sp': 'Region',
            # 'int_pc': '98765',
            'voice': '+30.2102125306',
            'fax': '+30.2102125306',
            'email': 'john.doe@example.com',
        }
        host_create = self.epp.host_create(host_info)
        if self.host_available:
            assert host_create is True, f"""expected host {self.host} to be created"""
        else:
            assert host_create is False, f"""expected host creation {self.host} to fail since its not available"""


    def test_host_update(self):
        host_info = {
            'host': self.host,
            'add' : {

            },
            'rem' : {

            },
            'chg' : {

            }
        }
        host_update = self.epp.host
        if self.host_available:
            assert ho
        else:
            assert contact_update is True, f"""expected contact {self.contact_id} to fail since its not available"""
    #
