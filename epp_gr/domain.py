from epp_gr import EppClient


class Domain:

    @staticmethod
    def check(epp: EppClient, domain_name: str) -> bool:
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
            return domain_name and domain_name.get('avail') == '1'  # '0' means exists, '1' means available
        return False

    @staticmethod
    def info(epp: EppClient, domain_name: str) -> dict:
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
                           'admin': soup.find('domain:contact', {'type': 'admin'}).text
                                    if soup.find('domain:contact', {'type': 'admin'}) else None,
                           'tech': soup.find('domain:contact', {'type': 'tech'}).text
                           if soup.find('domain:contact', {'type': 'tech'}) else None,
                           'billing': soup.find('domain:contact', {'type': 'billing'}).text
                           if soup.find('domain:contact', {'type': 'billing'}) else None,
                           'exp_date' : soup.find('')
                           }
            return domain_info

    @staticmethod
    def create(epp: EppClient, domain_info: dict) -> bool:
        xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
                <epp xmlns="urn:ietf:params:xml:ns:epp-1.0" 
                     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
                     xsi:schemaLocation="urn:ietf:params:xml:ns:epp-1.0 epp-1.0.xsd">
                    <command>
                        <create>
                            <domain:create 
                                 xmlns:domain="urn:ietf:params:xml:ns:domain-1.0" 
                                xsi:schemaLocation="urn:ietf:params:xml:ns:domain-1.0 domain-1.0.xsd">
                            <domain:name>{domain_info['name']}</domain:name>
                            <domain:period unit="y">{domain_info['period']}</domain:period>
                            <domain:registrant>{domain_info['registrant']}</domain:registrant>
                    """
        if domain_info.get('tech'):
            xml += f"""        <domain:contact type="tech">{domain_info['tech']}</domain:contact>"""
        if domain_info.get('admin'):
            xml += f"""        <domain:contact type="admin">{domain_info['admin']}</domain:contact>"""
        if domain_info.get('billing'):
            xml += f"""        <domain:contact type="billing">{domain_info['billing']}</domain:contact>"""
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
        return epp.last_result_code == '1001'

    @staticmethod
    def update(epp: EppClient, domain_info: dict) -> bool:
        xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
            <epp xmlns="urn:ietf:params:xml:ns:epp-1.0" 
                 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
                 xsi:schemaLocation="urn:ietf:params:xml:ns:epp-1.0 epp-1.0.xsd">
            <command>
                <update>
                    <domain:update xmlns:domain="urn:ietf:params:xml:ns:domain-1.0" 
                        xsi:schemaLocation="urn:ietf:params:xml:ns:domain-1.0 domain-1.0.xsd">
                        <domain:name>{domain_info['name']}</domain:name>
                            <domain:add>
                                <domain:ns>
                                    <domain:hostObj>{domain_info['host_add']}</domain:hostObj>
                                </domain:ns>
                                <domain:contact type="admin">{domain_info['admin_add']}</domain:contact>
                                <domain:contact type="tech">{domain_info['tech_add']}</domain:contact>
                                <domain:contact type="billing">{domain_info['billing_add']}</domain:contact>
                            </domain:add>
                            <domain:rem>
                                <domain:ns>
                                    <domain:hostObj>{domain_info['host_rem']}</domain:hostObj>
                                </domain:ns>
                                <domain:contact type="admin">{domain_info['admin_rem']}</domain:contact>
                                <domain:contact type="tech">{domain_info['tech_rem']}</domain:contact>
                                <domain:contact type="billing">{domain_info['billing_rem']}</domain:contact>
                            </domain:rem>        
                    </domain:update>
                </update>
            <clTRID>{epp.clTRID}</clTRID>
            </command>
            </epp>"""
        response, soup = epp.send_xml(xml)
        return epp.last_result_code == '1000'


    def delete(epp: EppClient, domain_name: str) -> bool:
        raise NotImplementedError


    def renew(epp: EppClient, domain_info: dict) -> dict:
        xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
            <epp xmlns="urn:ietf:params:xml:ns:epp-1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
                xsi:schemaLocation="urn:ietf:params:xml:ns:epp-1.0 epp-1.0.xsd">
                <command>
                    <renew>
                        <domain:renew xmlns:domain="urn:ietf:params:xml:ns:domain-1.0" 
                                xsi:schemaLocation="urn:ietf:params:xml:ns:domain-1.0 domain-1.0.xsd">
                            <domain:name>{domain_info['name']}r</domain:name>
                            <domain:curExpDate>{domain_info['current_exp_date']}</domain:curExpDate>
                            <domain:period unit="y">{domain_info['period']}</domain:period>
                    </domain:renew>
                    </renew>
                <clTRID>ABC:ics-forth:1079952249913</clTRID>
                </command>
            </epp>"""
        response, soup = epp.send_xml(xml)
        if epp.last_result_code == '1000':
            return  {'name': soup.find('domain:name').text,
                    'exp_date' : soup.find('domain:exDate').text}




