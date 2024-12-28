from unittest import TestCase
from epp_gr.EppClient import EppClient

class TestDomain(TestCase):

    registrant = 'arakas' # xxx_arakas must already exist
    domain_name = 'bizelaki.gr'
    domain_available = False

    def setUp(self):
        self.epp = EppClient()
        self.login_result = self.epp.login()

    def tearDown(self):
        self.epp.logout()

    def test_domain_check(self):
        domain_available = self.epp.domain_check(self.domain_name)
        # print(self.epp.last_payload)
        # self.epp.print_last_response()
        print(domain_available)
        assert domain_available is self.domain_available, f"domain {self.domain_available} exist is {self.domain_available}"

    def test_domain_info(self):
        domain_info = self.epp.domain_info(self.domain_name)
        if self.domain_available:
            assert domain_info is None
        else:
            self.epp.print_last_response()
            assert domain_info['name'] == self.domain_name , f"""domain  {self.domain_name} <> {domain_info['name']}"""


    def test_domain_create(self):
        domain_info = {
            'registrant': self.registrant,
            'name' : self.domain_name,
            'period' : '2',
        }
        domain_create = self.epp.domain_create(domain_info)
        self.epp.print_last_payload()

        # if self.domain_available:
        #     assert domain_create is True, f"""expected domain {self.domain_name} to be created {self.epp.last_response}"""
        # else:
        #     assert domain_create is False, f"""expected domain {self.domain_name} to fail since its not available {self.epp.last_response}"""

    def test_domain_update(self):
        domain_info = {
            'name' : 'bizelia.gr',

            # 'host_add' : 'ns.bizelia.gr',
            # 'admin_add' : 'b95_arakas',
            # 'tech_add' : 'b95_arakas',
            # 'billing_add' : 'b95_arakas',

            'host_rem' : 'ns.bizelia.gr',
            # 'admin_rem' : 'b95_arakas',
            # 'tech_rem' : 'b95_arakas',
            # 'billing_rem' :'b95_arakas',
        }


        self.epp.domain_update(domain_info)
        self.epp.print_last_payload()
        self.epp.print_last_response()



    def test_renew(self):
        # self.epp.print_last_payload()
        # print(self.epp.domain_info(self.domain_name))

        domain_info = {
             'name' : self.domain_name,
             'current_exp_date' : '2026-12-19',
            'period' : '2'
        }
        domain_renew = self.epp.domain_renew(domain_info)
        
        
        # print(domain_renew)
        print(self.epp.last_payload)
        print(self.epp.last_response)

    