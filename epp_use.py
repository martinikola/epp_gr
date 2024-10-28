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


for contact in contacts:
    print(epp.contact_info(contact))

# print(contact_info)