from bs4 import BeautifulSoup
from decouple import config
import requests
from _contact import _Contact

class EppClient:
    def __init__(self):
        self.contact = _Contact()


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


    # kind of facades
    def contact_check(self,contact_name:str):
        return self.contact.contact_check(self, contact_name )





