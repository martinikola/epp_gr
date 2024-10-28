from epp_gr.EppClient import EppClient

epp = EppClient()

epp.login()

# host="ns1.forth.gr"

contact_info = epp.contact_info('arakas3')


# epp.print_last_response()


print(contact_info)