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
                           # 'period': soup.find('domain:period').text, period does not exist on info...
                           'cr_date' : soup.find('domain:crDate').text,
                           'up_date' : soup.find('domain:upDate').text
                                if soup.find('domain:upDate') else None,
                           'exp_date': soup.find('domain:exDate').text
                           }
            return domain_info

    @staticmethod
    def create(epp: EppClient, domain_info: dict) -> dict:
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
                            <domain:registrant>{epp.prefix}_{domain_info['registrant']}</domain:registrant>
                    """
        if domain_info.get('tech'):
            xml += f"""        <domain:contact type="tech">{epp.prefix}_{domain_info['tech']}</domain:contact>"""
        if domain_info.get('admin'):
            xml += f"""        <domain:contact type="admin">{epp.prefix}_{domain_info['admin']}</domain:contact>"""
        if domain_info.get('billing'):
            xml += f"""        <domain:contact type="billing">{epp.prefix}_{domain_info['billing']}</domain:contact>"""
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
        if epp.last_result_code == '1001':
            created_domain_info = {
                           'result_code': epp.last_result_code,
                           'name': soup.find('domain:name').text,
                           'cr_date': soup.find('domain:crDate').text,
                           'exp_date': soup.find('domain:exDate').text
                           }
            return created_domain_info
        else:
            failed_domain_info = {
                'result_code': epp.last_result_code,
                'name': domain_info['name'],
                'result_msg': epp.last_result_msg,
                'comment': soup.find('extdomain:comment').text                
            }
            return failed_domain_info

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
                        <domain:name>{domain_info['name']}</domain:name>\n"""
        if any(key in domain_info for key in ['host_add', 'admin_add', 'tech_add', 'billing_add']):
            xml += f"""                        <domain:add>\n"""
        if 'host_add' in domain_info:
            xml += f"""                        <domain:ns><domain:hostObj>{domain_info['host_add']}</domain:hostObj></domain:ns>\n"""
        if 'admin_add' in domain_info:
            xml += f"""                        <domain:contact type="admin">{epp.prefix}_{domain_info['admin_add']}</domain:contact>\n"""
        if 'tech_add' in domain_info:
            xml += f"""                        <domain:contact type="tech" >{epp.prefix}_{domain_info['tech_add']}</domain:contact>\n"""
        if 'billing_add' in domain_info:
            xml += f"""                        <domain:contact type="billing">{epp.prefix}_{domain_info['billing_add']}</domain:contact>\n"""
        if any(key in domain_info for key in ['host_add', 'admin_add', 'tech_add', 'billing_add']):
            xml += f"""                        </domain:add>\n"""
        if any(key in domain_info for key in ['host_rem', 'admin_rem', 'tech_rem', 'billing_rem']):
            xml += f"""                        <domain:rem>\n"""
        if 'host_rem' in domain_info:
            xml += f"""                        <domain:ns><domain:hostObj>{domain_info['host_rem']}</domain:hostObj></domain:ns>\n"""
        if 'admin_rem' in domain_info:
            xml += f"""                        <domain:contact type="admin">{epp.prefix}_{domain_info['admin_rem']}</domain:contact>\n"""
        if 'tech_rem' in domain_info:
            xml += f"""                        <domain:contact type="tech">{epp.prefix}_{domain_info['tech_rem']}</domain:contact>\n"""
        if 'billing_rem' in domain_info:
            xml += f"""                        <domain:contact type="billing">{epp.prefix}_{domain_info['billing_rem']}</domain:contact>\n"""
        if any(key in domain_info for key in ['host_rem', 'admin_rem', 'tech_rem', 'billing_rem']):
            xml += f"""                        </domain:rem>\n"""

        xml += f"""                        </domain:update>
                </update>
            <clTRID>{epp.clTRID}</clTRID >
            </command>
            </epp>"""
        response, soup = epp.send_xml(xml)
        return epp.last_result_code == '1000'


    def delete(epp: EppClient, domain_name: str) -> bool:
        raise NotImplementedError


    def renew(epp: EppClient, domain_info: dict) -> dict:
        xml = f"""<?xml version = "1.0" encoding = "UTF-8" standalone = "no"?>
               <epp xmlns = "urn:ietf:params:xml:ns:epp-1.0"
                    xmlns:xsi = "http://www.w3.org/2001/XMLSchema-instance"
                    xsi:schemaLocation = "urn:ietf:params:xml:ns:epp-1.0 epp-1.0.xsd" >
                    <command>
                        <renew>
                        <domain:renew xmlns:domain = "urn:ietf:params:xml:ns:domain-1.0"
                                xsi:schemaLocation = "urn:ietf:params:xml:ns:domain-1.0 domain-1.0.xsd" >
                            <domain:name>{domain_info['name']}</domain:name>
                            <domain:curExpDate>{domain_info['current_exp_date']}</domain:curExpDate >
                            <domain:period unit="y">{domain_info['period']}</domain:period >
                        </domain:renew>
                        </renew>
                    <clTRID>{epp.clTRID}</clTRID >
                    </command>
               </epp>"""
        response, soup = epp.send_xml(xml)
        if epp.last_result_code == '1000':
            return  {'result_code': epp.last_result_code,
                    'result_msg': epp.last_result_msg,
                
                    'name': soup.find('domain:name').text,
                    'exp_date' : soup.find('domain:exDate').text}
        else:
            return {'result_code': epp.last_result_code,
                    'result_msg': epp.last_result_msg,
                    
                    }                    
