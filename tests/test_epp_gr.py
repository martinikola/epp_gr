from unittest import TestCase
from epp_gr import EppClient


class TestEppClient(TestCase):

    def setUp(self):
        self.epp = EppClient()
        self.login_result = self.epp.login()

    def test_successful_login(self):
        login_result = self.epp.login()
        self.epp.print_last_response()
        assert login_result, True

    def test_failed_login(self):
        self.epp.pw = 'bananas'
        login_result = self.epp.login()
        assert login_result, False

    def test_contact_check(self):
        self.epp.contact_check('arakas')
