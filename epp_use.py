from soupsieve.pretty import pretty

from epp_gr.EppClient import EppClient

epp = EppClient()

epp.login()

print(epp.domain_info("bizelaki.gr"))

# epp.print_last_response()


