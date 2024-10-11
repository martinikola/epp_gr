from epp_gr.EppClient import EppClient

epp = EppClient()

epp.login()

# host="ns1.forth.gr"

hosts = [
    # "ns.arakas.gr", "ns.bizeli.gr", "ns.bizelia.gr",
    "psakse.bizelia.gr",
    "ns.forth.gr", "ns1.forth.gr",
    "ns.paparas.gr",
    "ns.bizeli.gr"
]


for host in hosts:
    print(f"***** {host} *****)")
    print(f"available : {epp.host_check(host)} ")
    print(f"info : {epp.host_info(host) }" )