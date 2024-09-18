from epp_gr import EppClient

class Contact:

    @staticmethod
    def check(epp: EppClient, contact_name:str) -> bool:
        """ checks the availability  of a contacts returns True if exists"""
        xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
            <epp xmlns="urn:ietf:params:xml:ns:epp-1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
                xsi:schemaLocation="urn:ietf:params:xml:ns:epp-1.0 epp-1.0.xsd">
                <command>
                    <check>
                        <contact:check xmlns:contact="urn:ietf:params:xml:ns:contact-1.0" 
                            xsi:schemaLocation="urn:ietf:params:xml:ns:contact-1.0 contact-1.0.xsd">
                            <contact:id>{contact_name}</contact:id>
                        </contact:check>
                    </check>
                <clTRID>{epp.clTRID}</clTRID>
                </command>
            </epp>"""
        response, soup = epp.send_xml(xml)
        if epp.last_result_code == '1000':
            contact_id = soup.find('contact:id')
            return contact_id and contact_id.get('avail') == '0'  # '0' means exists, '1' means available
        return False


    @staticmethod
    def info(epp: EppClient, contact_id:str) -> dict:
        """ get contact info """
        xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
        <epp xmlns="urn:ietf:params:xml:ns:epp-1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xsi:schemaLocation="urn:ietf:params:xml:ns:epp-1.0 epp-1.0.xsd">
            <command>
                <info>
                    <contact:info
                    xmlns:contact="urn:ietf:params:xml:ns:contact-1.0"
                    xsi:schemaLocation="urn:ietf:params:xml:ns:contact-1.0
                    contact-1.0.xsd">
                        <contact:id>{epp.prefix}_{contact_id}</contact:id>

                    </contact:info>
                </info>
                <clTRID>{epp.clTRID}</clTRID>
            </command>
        </epp>"""
        response, soup = epp.send_xml(xml)
        if epp.last_result_code == '1000':
            contact_info = {'contact_id': soup.find('contact:id').text,
                            'roid': soup.find('contact:roid').text}
            postal_loc = soup.find("contact:postalInfo", {"type": "loc"})
            contact_info['loc_name'] = postal_loc.find('contact:name').text
            contact_info['loc_org'] = postal_loc.find('contact:org').text
            loc_street_elements = postal_loc.find_all('contact:street')
            for i, loc_street in enumerate(loc_street_elements, start=1):
                contact_info[f'loc_street{i}'] = loc_street.get_text(strip=True)
            contact_info['loc_city'] = postal_loc.find('contact:city').text
            contact_info['loc_sp'] = postal_loc.find('contact:sp').text
            contact_info['loc_pc'] = postal_loc.find('contact:pc').text
            return contact_info

    @staticmethod
    def contact_create(epp: EppClient, contact_info:dict) -> bool:
        xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
                    <epp xmlns="urn:ietf:params:xml:ns:epp-1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="urn:ietf:params:xml:ns:epp-1.0 epp-1.0.xsd">
                        <command>
                            <create>
                                <contact:create xmlns:contact="urn:ietf:params:xml:ns:contact-1.0" xsi:schemaLocation="urn:ietf:params:xml:ns:contact-1.0 contact-1.0.xsd">
                                    <contact:id>{epp.prefix}_{contact_info['contact_id']}</contact:id>
                                    <contact:postalInfo type="loc">
                                        <contact:name>{contact_info['loc_name']}</contact:name>
                                        <contact:org>{contact_info['loc_org']}</contact:org>
                                        <contact:addr>
                                            <contact:street>{contact_info['loc_street1']}</contact:street>
                                            <contact:street>{contact_info['loc_street2']}</contact:street>
                                            <contact:street>{contact_info['loc_street3']}</contact:street>
                                            <contact:city>{contact_info['loc_city']}</contact:city>
                                            <contact:sp>{contact_info['loc_sp']}</contact:sp>
                                            <contact:pc>{contact_info['loc_pc']}</contact:pc>
                                            <contact:cc>{contact_info['loc_cc']}</contact:cc>
                                        </contact:addr>
                                    </contact:postalInfo>
                                    <contact:voice x="">{contact_info['voice']}</contact:voice>
                                    <contact:fax x="">{contact_info['fax']}</contact:fax>
                                    <contact:email>{contact_info['email']}</contact:email>
                                    <contact:authInfo>
                                        <contact:pw></contact:pw>
                                    </contact:authInfo>
                                    <contact:disclose flag="0">
                                        <contact:name type="int" />
                                        <contact:name type="loc" />
                                        <contact:org type="int" />
                                        <contact:org type="loc" />
                                        <contact:addr type="int" />
                                        <contact:addr type="loc" />
                                        <contact:voice />
                                        <contact:fax />
                                        <contact:email />
                                    </contact:disclose>
                                </contact:create>
                            </create>
                            <clTRID>{epp.clTRID}</clTRID>
                        </command>
                    </epp>"""
        response, soup = epp.send_xml(xml)
        return epp.last_result_code == '1000'

    @staticmethod
    def contact_update(epp: EppClient, contact_info:dict) -> bool:
        """ contact update  """
        xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
                <epp xmlns="urn:ietf:params:xml:ns:epp-1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="urn:ietf:params:xml:ns:epp-1.0 epp-1.0.xsd">
                <command>
                    <update>
                    <contact:update
                        xmlns:contact="urn:ietf:params:xml:ns:contact-1.0" 
                            xsi:schemaLocation="urn:ietf:params:xml:ns:contact-1.0 
                            contact-1.0.xsd">
                        <contact:id>{epp.prefix}_{contact_info['contact_id']}</contact:id>
                        <contact:chg>
                        <contact:postalInfo type="loc">
                            <contact:addr>
                                <contact:street>{contact_info['loc_street1']}</contact:street>
                                <contact:street>{contact_info['loc_street2']}</contact:street>
                                <contact:street>{contact_info['loc_street3']}</contact:street>
                                <contact:city>{contact_info['loc_city']}</contact:city>
                                <contact:sp>{contact_info['loc_sp']}</contact:sp>
                                <contact:pc>{contact_info['loc_pc']}</contact:pc>
                                <contact:cc>{contact_info['loc_cc']}</contact:cc>
                            </contact:addr>
                        </contact:postalInfo>
                        <contact:voice x="">{contact_info['voice']}</contact:voice>
                        <contact:fax x="">{contact_info['fax']}</contact:fax>
                        <contact:email>{contact_info['email']}</contact:email>
                        </contact:chg>
                    </contact:update>
                    </update>     
                </command>
                </epp>"""
        response, soup = epp.send_xml(xml)
        return epp.last_result_code == '1000'















