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
        successful_login = self.epp.login()
        assert successful_login is True, "login was successful"

    def test_failed_login(self):
        self.epp.pw = 'bananas'
        failed_login = self.epp.login()
        assert failed_login is False, "login was not successful"

