from unittest import TestCase
from epp_gr.EppClient import EppClient

class TestContact(TestCase):

    contact_id = "arakas"
    contact_available = False

    def setUp(self):
        self.epp = EppClient()
        self.login_result = self.epp.login()

    def tearDown(self):
        self.epp.logout()

    def test_contact_check(self):
        contact_available = self.epp.contact_check(self.contact_id)
        self.epp.print_last_response()
        # assert contact_available is self.contact_available, f"contact {self.contact_id} exist is {self.contact_available}"

    def test_contact_info(self):
        contact_info = self.epp.contact_info(self.contact_id)
        if self.contact_available:
            assert contact_info is None
        else:
            epp_contact_id  = self.epp.prefix + "_" + self.contact_id
            assert contact_info['contact_id'] == epp_contact_id , f"""contact {self.contact_id} <> {epp_contact_id}"""


    def test_contact_create(self):
        contact_info = {
            'contact_id': self.contact_id,
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
        contact_create = self.epp.contact_create(contact_info)
        if self.contact_available:
            assert contact_create is True, f"""expected contact {self.contact_id} to be created"""
        else:
            assert contact_create is False, f"""expected contact {self.contact_id} to fail since its not available"""



    def test_contact_update(self):
        contact_info = {
            'contact_id': self.contact_id,
            # loc_name, loc_org, int_name , int_org not updatable
            'loc_street1': 'ΑΧΑΡΝΩΝ',
            'loc_street2': 'ΠΑΠΑΦΛΕΣΣΑ',
            'loc_street3': 'ΕΔΩ ΣΟΥ ξανα - ΑΛΛΑΖΩ ΤΑ ΦΩΡΤΑ',
            'loc_city': 'ΑΘΗΝΑ',
            'loc_sp': 'ΠΕΙΡΑΙΑΣ',
            'loc_pc': '12345',
            'voice': '+30.2102125306',
            'fax': '+30.2102125306',
            'email': 'john.doe@example.com',
            'loc_cc': 'cr'
        }
        # recheck since create may have succeeded
        contact_available_now = self.epp.contact_check(self.contact_id)
        contact_update = self.epp.contact_update(contact_info)
        # if contact_available_now (meaning DOES NOT exist) i can update it
        if contact_available_now:
            assert contact_update is False, f"""expected contact {self.contact_id} to be updated"""
        else:
            assert contact_update is True, f"""expected contact {self.contact_id} to fail since its not available"""

