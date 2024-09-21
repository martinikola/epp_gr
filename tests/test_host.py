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
            'ip_v4': '13.13.13.13',
            'ip_v6': '1080:0:0:0:8:800:200C:417A'
        }
        host_create = self.epp.host_create(host_info)
        if self.host_available:
            assert host_create is True, f"""expected host {self.host} to be created"""
        else:
            assert host_create is False, f"""expected host creation {self.host} to fail since its not available"""

    def test_host_update(self):
        host_info = {
            'host': self.host,
            'add': {

            },
            'rem': {

            },
            'chg': {

            }
        }
        host_update = self.epp.host_create(host_info)
        if self.host_available:
            assert host_update is True
        else:
            assert host_update is False, f"""expected host {self.host_available} to fail since its not available"""

