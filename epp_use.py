from soupsieve.pretty import pretty

from epp_gr.EppClient import EppClient

epp = EppClient()

epp.login()

# host="ns1.forth.gr"
contacts = [
     "arakas", "arakas1", "arakas2", "arakas3", "arakas33", "arakas34", "bizeli",
     "fani", "fanucom", "fanucom1", "fanucom2", "fanucom3",
     "nikos", "nikos1", "nikos2", "nikolakis","nikolakis1", "nikolakis2","nikolakis3",
     "digitalgov","cure","arakas43", "arakas99", "kikirikou", "louloudaki", "sougia2024",
    "tornado", "kardistan", "cnectF4"
 ]


hosts = [
    "ns.arakas.gr", "ns.bizeli.gr", "ns.bizelia.gr", "ns.arambas.gr"
    "psakse.bizelia.gr","ns.bizelia.gr",
     "ns.forth.gr", "ns1.forth.gr",
    "ns.papakia.gr","ns1.papakia.gr","ns2.papakia.gr","ns3.papakia.gr","ns6.papakia.gr"
]

# for contact in contacts:
#     print(epp.contact_info(contact))

# print(contact_info)


for host in hosts:
    print(pretty(epp.host_info(host)))


# host_info = epp.host_info('ns.arakas.gr')
#
# # epp.print_last_response()
#
#
#
# print(pretty(host_info))