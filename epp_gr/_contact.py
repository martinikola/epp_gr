from epp_gr import EppClient

__all__ = ['_Contact']

class _Contact:

    def contact_check(self, epp: EppClient, contact_name:str) -> bool:
        """ checks the availability  of a contacts returns True if exists"""
        xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
            <epp xmlns="urn:ietf:params:xml:ns:epp-1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
                xsi:schemaLocation="urn:ietf:params:xml:ns:epp-1.0 epp-1.0.xsd">
                <command>
                    <check>
                        <contact:check xmlns:contact="urn:ietf:params:xml:ns:contact-1.0" 
                            xsi:schemaLocation="urn:ietf:params:xml:ns:contact-1.0 contact-1.0.xsd">
                            {contact_name}
                        </contact:check>
                    </check>
                <clTRID>{epp.clTRID}</clTRID>
                </command>
            </epp>"""