from soupsieve.pretty import pretty

from epp_gr.EppClient import EppClient

epp = EppClient()

epp.login()




info = epp.domain_info('bizeli.gr')

epp.print_last_response()

print(pretty(info))

