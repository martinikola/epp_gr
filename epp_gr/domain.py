from epp_gr import EppClient

class Domain:

    @staticmethod
    def domain_check(epp: EppClient, domain_name:str) -> bool:
        """ checks the availability  of a domain returns True if exists"""
        xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
                <epp xmlns="urn:ietf:params:xml:ns:epp-1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="urn:ietf:params:xml:ns:epp-1.0 epp-1.0.xsd">
                <command>
                    <check>
                        <domain:check xmlns:domain="urn:ietf:params:xml:ns:domain-1.0" xsi:schemaLocation="urn:ietf:params:xml:ns:domain-1.0 domain-1.0.xsd">
                        <domain:name>{domain_name}</domain:name>
                    </domain:check>
                    </check>
                <clTRID>{epp.clTRID}</clTRID>
                </command>
                </epp>"""
        response, soup = epp.send_xml(xml)
        if epp.last_result_code == '1000':
            domain_name = soup.find('domain:name')
            return domain_name and domain_name.get('avail') == '0'  # '0' means exists, '1' means available
        return False


    @staticmethod
    def domain_info(epp: EppClient, domain_name:str) -> dict:
        """ get domain info or error if not exists"""
        xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
                <epp xmlns="urn:ietf:params:xml:ns:epp-1.0" 
                    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
                    xsi:schemaLocation="urn:ietf:params:xml:ns:epp-1.0 epp-1.0.xsd">
                    <command>
                        <info>
                            <domain:info xmlns:domain="urn:ietf:params:xml:ns:domain-1.0" 
                                    xsi:schemaLocation="urn:ietf:params:xml:ns:domain-1.0 domain-1.0.xsd">
                            <domain:name hosts="all">{domain_name}</domain:name>
                            <domain:authInfo>
                            <domain:pw></domain:pw>
                            </domain:authInfo>
                            </domain:info>
                        </info>
                        <clTRID>{epp.clTRID}</clTRID>
                    </command>
                </epp>"""
        response, soup = epp.send_xml(xml)
        if epp.last_result_code == '1000':
            domain_info = {'name': soup.find('domain:name').text,
                           'roid': soup.find('domain:roid').text,
                           'registrant': soup.find('domain:registrant').text,
                           'admin': soup.find('domain:contact', {'type': 'admin'}).text}
            return domain_info

    @staticmethod
    def create_domain(epp: EppClient, domain:dict) -> bool:
        xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
                <epp xmlns="urn:ietf:params:xml:ns:epp-1.0" 
                     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
                     xsi:schemaLocation="urn:ietf:params:xml:ns:epp-1.0 epp-1.0.xsd">
                    <command>
                        <create>
                            <domain:create 
                                 xmlns:domain="urn:ietf:params:xml:ns:domain-1.0" 
                                xsi:schemaLocation="urn:ietf:params:xml:ns:domain-1.0 domain-1.0.xsd">
                            <domain:name>{domain['name']}</domain:name>
                            <domain:period unit="y">{domain['period']}</domain:period>
                            <domain:registrant>{domain['registrant']}</domain:registrant>
                    """
        if 'tech' in domain:
            xml += f"""        <domain:contact type="tech">{domain['tech']}</domain:contact>"""
        if 'admin' in domain:
            xml += f"""        <domain:contact type="admin">{domain['admin']}</domain:contact>"""
        if 'billing' in domain:
            xml += f"""        <domain:contact type="billing">{domain['billing']}</domain:contact>"""
        xml += f"""<domain:authInfo>
                                <domain:pw/>
                            </domain:authInfo>
                            </domain:create>
                        </create>
                        <clTRID>{epp.clTRID}</clTRID>
                    </command>
                </epp>
                """
        response, soup = epp.send_xml(xml)
        return epp.last_result_code == '1000'

    @staticmethod
    def domain_update(epp: EppClient, contact_info:dict) -> bool:
        xml = ""
        response, soup = epp.send_xml(xml)
        return epp.last_result_code == '1000'















