from soupsieve.pretty import pretty

from epp_gr.EppClient import EppClient

epp = EppClient()

epp.login()

# epp.print_last_response()

domains = [
    "bizeli.gr","arakas.gr","digitalgov.gr","cureforall.gr", "nikolakis.gr", "saxlamaras.gr", "banana.gr", "spareparts.edu.gr"

]

for domain in domains:
    print(epp.domain_info(domain))
