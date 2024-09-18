from unittest import TestCase
from epp_gr.EppClient import EppClient


# REGISTRAR_URL="https://uat-regepp.ics.forth.gr:700/epp/proxy"
# REGISTRAR_CLID="acropolis1"
# REGISTRAR_PW="*Peiraios*24"
# REGISTRAR_CLTRID="acro"
# REGISTRAR_PREFIX="b95"


class TestEppClient(TestCase):

    def setUp(self):
        self.epp = EppClient()
        self.login_result = self.epp.login()

    def test_successful_login(self):
        login_result = self.epp.login()
        # self.epp.print_last_response()
        assert login_result, True

    def test_failed_login(self):
        self.epp.pw = 'bananas'
        login_result = self.epp.login()
        self.epp.print_last_response()
        assert login_result, False

    def test_contact_check(self):
        self.epp.contact_check('arakas')


    def test_contact_create(self):
        self.epp.contact_create('arakas')
