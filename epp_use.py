from soupsieve.pretty import pretty

from epp_gr.EppClient import EppClient

epp = EppClient()

epp.login()



domain_info = {
            'registrant': 'c27_Eustat50',
            'name' : 'bizelaki.gr',
            'period' : '2',
        }

domain_create = epp.domain_create(domain_info)
print(domain_create)

from bs4 import BeautifulSoup, version


print(BeautifulSoup.ve)