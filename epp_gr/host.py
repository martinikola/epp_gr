from epp_gr import EppClient

class Host:

    @staticmethod
    def host_check(epp: EppClient, host_name:str) -> bool:
        """ checks the availability  of a host returns True if exists"""
        xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
                <epp xmlns="urn:ietf:params:xml:ns:epp-1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="urn:ietf:params:xml:ns:epp-1.0 epp-1.0.xsd">
                <command>
                    <check>
                    <host:check xmlns:host="urn:ietf:params:xml:ns:host-1.0" 
                        xsi:schemaLocation="urn:ietf:params:xml:ns:host-1.0 host-1.0.xsd">
                        <host:name>{host_name}</host:name>
                    </host:check>
                    </domain:check>
                    </check>
                <clTRID>{epp.clTRID}</clTRID>
                </command>
                </epp>"""
        response, soup = epp.send_xml(xml)
        if epp.last_result_code == '1000':
            host_name = soup.find('domain:name')
            return host_name and host_name.get('avail') == '0'  # '0' means exists, '1' means available
        return False


    @staticmethod
    def host_info(epp: EppClient, host_name:str) -> dict:
        """ get host info or error if not exists"""
        xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
                <epp xmlns="urn:ietf:params:xml:ns:epp-1.0" 
                    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
                    xsi:schemaLocation="urn:ietf:params:xml:ns:epp-1.0 epp-1.0.xsd">
                    <command>
                        <info>
                            <host:info xsi:schemaLocation="urn:ietf:params:xml:ns:host-1.0 host-1.0.xsd" 
                                xmlns:host="urn:ietf:params:xml:ns:host-1.0">
                        <host:name>{host_name}r</host:name>
                        </host:info>
                        </info>
                        <clTRID>{epp.clTRID}</clTRID>
                    </command>
                </epp>"""
        response, soup = epp.send_xml(xml)
        if epp.last_result_code == '1000':
            host_info = {'name': soup.find('host:name').text,
                           'roid': soup.find('host:roid').text}
            ip_v4 = soup.find('host:addr', {'ip':'v4'})
            if ip_v4:
                host_info['ip_v4'] = ip_v4.text
            ip_v6 = soup.find('host:addr', {'ip': 'v4'})
            if ip_v6:
                host_info['ip_v6'] = ip_v6.text
            return host_info

    @staticmethod
    def create_host(epp: EppClient, host:dict) -> bool:
        xml = ""
        response, soup = epp.send_xml(xml)
        return epp.last_result_code == '1000'

    @staticmethod
    def host_update(epp: EppClient, host:dict) -> bool:

        response, soup = epp.send_xml(xml)
        return epp.last_result_code == '1000'















