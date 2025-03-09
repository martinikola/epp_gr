from ipaddress import ip_address
from epp_gr import EppClient


class Host:

    @staticmethod
    def check(epp: EppClient, host_name: str) -> bool:
        """ checks the availability  of a host returns True if exists"""
        xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
                <epp xmlns="urn:ietf:params:xml:ns:epp-1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="urn:ietf:params:xml:ns:epp-1.0 epp-1.0.xsd">
                <command>
                    <check>
                        <host:check xmlns:host="urn:ietf:params:xml:ns:host-1.0"
                        xsi:schemaLocation="urn:ietf:params:xml:ns:host-1.0 host-1.0.xsd">
                        <host:name>{host_name}</host:name>
                        </host:check>
                    </check>
                <clTRID>{epp.clTRID}</clTRID>
                </command>
                </epp>"""
        response, soup = epp.send_xml(xml)
        if epp.last_result_code == '1000':
            host_name = soup.find('host:name')
            # '0' means exists, '1' means available
            return host_name and host_name.get('avail') == '1'
        return False

    @staticmethod
    def info(epp: EppClient, host_name: str) -> dict:
        """ get host info or error if not exists"""
        xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
                <epp xmlns="urn:ietf:params:xml:ns:epp-1.0"
                    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                    xsi:schemaLocation="urn:ietf:params:xml:ns:epp-1.0 epp-1.0.xsd">
                    <command>
                        <info>
                            <host:info xsi:schemaLocation="urn:ietf:params:xml:ns:host-1.0 host-1.0.xsd"
                                xmlns:host="urn:ietf:params:xml:ns:host-1.0">
                        <host:name>{host_name}</host:name>
                        </host:info>
                        </info>
                        <clTRID>{epp.clTRID}</clTRID>
                    </command>
                </epp>"""
        response, soup = epp.send_xml(xml)
        if epp.last_result_code == '1000':
            host_info = {'name': soup.find('host:name').text, 'roid': soup.find('host:roid').text,
                         'ip_addresses': [addr.text.strip()
                                          for addr in soup.find_all('host:addr')]}
            # ip_v4 = soup.find('host:addr', {'ip':'v4'})
            # if ip_v4:
            #     host_info['ip_v4'] = ip_v4.text
            # ip_v6 = soup.find('host:addr', {'ip': 'v6'})
            # if ip_v6:
            #     host_info['ip_v6'] = ip_v6.text
            # host_info['ip_address'] = host_info['ip_addresses'][0] if host_info['ip_addresses'] else None
            return host_info

    @staticmethod
    def create(epp: EppClient, host: dict) -> bool:
        # xml = f"""
        # <?xml version="1.0" encoding="UTF-8" standalone="no"?>
        # <epp xsi:schemaLocation="urn:ietf:params:xml:ns:epp-1.0 epp-1.0.xsd"
        #         xmlns="urn:ietf:params:xml:ns:epp-1.0"
        #         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        #     <command>
        #         <create>
        #         <host:create xsi:schemaLocation="urn:ietf:params:xml:ns:host-1.0 host-1.0.xsd"
        #             xmlns:host="urn:ietf:params:xml:ns:host-1.0">
        #             <host:name>ns1.forth.gr</host:name>
        #             <host:addr ip="v6">1080:0:0:0:8:800:200C:417A</host:addr>
        #             <host:addr>11.1.1.1</host:addr>
        #         </host:create>
        #         </create>
        #     <clTRID>ABC:ics-forth:1079691187887</clTRID>
        # </command>
        # </epp>"""
        xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
            <epp xsi:schemaLocation="urn:ietf:params:xml:ns:epp-1.0 epp-1.0.xsd"
                xmlns="urn:ietf:params:xml:ns:epp-1.0"
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            <command>
                <create>
                    <host:create xsi:schemaLocation="urn:ietf:params:xml:ns:host-1.0 host-1.0.xsd"
                        xmlns:host="urn:ietf:params:xml:ns:host-1.0">
                    <host:name>{host['name']}</host:name>"""
        if 'ip_v6' in host:
            xml += f"""<host:addr ip="v6">{host['ip_v6']}</host:addr>"""
        if 'ip_v4' in host:
            xml += f"""<host:addr>{host['ip_v4']}</host:addr>"""

        xml += f"""</host:create>
                </create>
                <clTRID>{epp.clTRID}</clTRID>
            </command>
            </epp>"""
        response, soup = epp.send_xml(xml)
        return epp.last_result_code == '1000'

    @staticmethod
    def update(epp: EppClient, host: dict) -> bool:
        xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
        <epp xmlns="urn:ietf:params:xml:ns:epp-1.0"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xsi:schemaLocation="urn:ietf:params:xml:ns:epp-1.0 epp-1.0.xsd">
            <command>
                <update>
                    <host:update xmlns:host="urn:ietf:params:xml:ns:host-1.0"
                        xsi:schemaLocation="urn:ietf:params:xml:ns:host-1.0 host-1.0.xsd">
                        <host:name>ns1.forth.gr</host:name>
                        <host:add>
                            <host:addr ip="v4">11.11.11.11</host:addr>
                        </host:add>
                        <host:rem>
                        <!-- default ip type is v4 -->
                            <host:addr>200.200.200.211</host:addr>
                        </host:rem>
                        <host:chg>
                            <host:name>new.forth.gr</host:name>
                        </host:chg>
                    </host:update>
                </update>
                <clTRID>ABC:ics-forth:1079699022918</clTRID>
            </command>
        </epp>"""
        response, soup = epp.send_xml(xml)
        if epp.last_result_code == '1000':
            return True

    @staticmethod
    def delete(epp: EppClient, host_name:str) -> bool:
        xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
            <epp xmlns="urn:ietf:params:xml:ns:epp-1.0"
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                xsi:schemaLocation="urn:ietf:params:xml:ns:epp-1.0 epp-1.0.xsd">
                <command>
                    <delete>
                        <host:delete xmlns:host="urn:ietf:params:xml:ns:host-1.0"
                            xsi:schemaLocation="urn:ietf:params:xml:ns:host-1.0 host-1.0.xsd">
                        <host:name>{host_name}</host:name>
                        </host:delete>
                    </delete>
                    <clTRID>{epp.clTRID}</clTRID>
                </command>
            </epp>"""
        response, soup = epp.send_xml(xml)
        if epp.last_result_code == '1000':
                return True
