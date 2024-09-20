from bs4 import BeautifulSoup
from decouple import config
import requests

from epp_gr.contact import Contact


class EppClient:

    # def __init__(self):
    # from epp_gr.contact import Contact
    # self.contact = Contact

    url = config("REGISTRAR_URL")
    clID = config("REGISTRAR_CLID")
    pw = config("REGISTRAR_PW")
    clTRID = config("REGISTRAR_CLTRID")
    prefix = config("REGISTRAR_PREFIX")

    jsessionid = ""

    last_response = ""
    last_result_code = ""
    last_result_msg = ""
    last_payload = ""

    def print_last_response(self):
        print(self.last_response)

    def send_xml(self,xml):
        headers = {'Content-Type': 'application/xml', 'Connection': 'keep-alive',
                   'Cookie': 'JSESSIONID=' + self.jsessionid + '; Path=/epp; Secure; HttpOnly;'}
        self.last_payload = xml
        response = requests.request(
            "GET", self.url, headers=headers, data=xml.encode('utf-8'))
        if response:
            soup = BeautifulSoup(response.text, 'xml')
            self.last_result_code = soup.find('result')['code']
            self.last_result_msg = soup.find('result').find('msg')
            self.last_response = soup.prettify()
            return response, soup

    def hello(self):
        xml = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
                <epp xmlns="urn:ietf:params:xml:ns:epp-1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
                    xsi:schemaLocation="urn:ietf:params:xml:ns:epp-1.0 epp-1.0.xsd">
                    <hello/>
                </epp>"""
        self.send_xml(xml)

    def login(self):
        """ logins to epp service """
        xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
                <epp xmlns="urn:ietf:params:xml:ns:epp-1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                    xsi:schemaLocation="urn:ietf:params:xml:ns:epp-1.0 epp-1.0.xsd">
                    <command>
                        <login>
                            <clID>{self.clID}</clID>
                            <pw>{self.pw}</pw>
                            <options>
                                <version>1.0</version>
                                <lang>en</lang>
                            </options>
                            <svcs>
                                <objURI>urn:ietf:params:xml:ns:host-1.0</objURI>
                                <objURI>urn:ietf:params:xml:ns:contact-1.0</objURI>
                                <objURI>urn:ietf:params:xml:ns:domain-1.0</objURI>
                            </svcs>
                        </login>
                        <clTRID>{self.clTRID}</clTRID>
                    </command>
                </epp>"""
        response, soup = self.send_xml(xml)
        if self.last_result_code == '1000':
            self.jsessionid = response.cookies.get('JSESSIONID')
            return True
        else:
            return False


    def logout(self):
        """ logout current session"""
        xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
                <epp xmlns="urn:ietf:params:xml:ns:epp-1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
                    xsi:schemaLocation="urn:ietf:params:xml:ns:epp-1.0 epp-1.0.xsd">
                    <command>
                        <logout/>
                        <clTRID>{self.clTRID}</clTRID>
                    </command>
                </epp>"""
        response, soup = self.send_xml(xml)
        if self.last_result_code == '1000':
            return True
        else:
            return False


    def contact_check(self,contact_name:str) -> bool:
        """ checks the availability  of a contacts returns True if available else False """
        # return self.contact.contact_check(self, contact_name )
        from epp_gr.contact import Contact
        return Contact.check(self,contact_name)

    def contact_info(self,contact_name:str) -> dict:
        from epp_gr.contact import Contact
        return Contact.info(self,contact_name)

    def contact_create(self, contact_info:dict) -> bool:
        from epp_gr.contact import Contact
        return Contact.contact_create(self,contact_info)

    def contact_update(self,contact_info:dict) -> bool:
        from epp_gr.contact import Contact
        return Contact.contact_update(self,contact_info)



    def host_check(self,host_name:str) -> bool:
        """ checks the availability  of a host returns True if available else False """
        from epp_gr.host import Host
        return Host.host_check(self, host_name)

    def host_info(self,host_name:str) -> dict
        """ retrieves the host information """
        from epp_gr.host import Host
        return Host.host_info(self, host_name)

    def host_create(self, host_info:dict) -> bool:
        from epp_gr.host import Host
        return Host.create_host(self, host_info)



