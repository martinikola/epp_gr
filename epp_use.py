from epp_gr.EppClient import EppClient

epp = EppClient()

epp.login()

# host="ns1.forth.gr"

hosts = [
    "ns.arakas.gr", "ns.bizeli.gr", "ns.bizelia.gr", "psakse.bizelia.gr"
]


for host in hosts:
    print(epp.host_info(host))