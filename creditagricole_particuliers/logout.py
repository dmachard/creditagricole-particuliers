import requests
import os
import json

class Logout:
    def __init__(self, session):
        """
        Initialize logout process
        
        Args:
            session (Authenticator): Authentication session
        """
        self.session = session
        self.logout()
        
    def logout(self):
        """
        Perform the logout operation to close the session with the bank
        
        Returns:
            bool: True if logout was successful
            
        Raises:
            Exception: If the API request fails
        """
        mock_file_base = "logout"
        
        if self.session.useMocks:
            # Use the new read_json_mock method
            self.session.mock_config.read_json_mock(f"{mock_file_base}_{self.session.mock_config.useMockSuffix}.json")
        else:
            url = "%s" % self.session.url
            url += "/%s/particulier.npc.logout.html?resource=" % self.session.regional_bank_url
            url += "/content/ca/cr866/npc/fr/particulier.html"
            r = requests.get(url=url,
                            verify=self.session.ssl_verify,
                            cookies=self.session.cookies)
            if r.status_code != 200:
                raise Exception( "[error] logout: %s - %s" % (r.status_code, r.text) )
            
        # Write mock data if requested
        if self.session.writeMocks:
            # Use the new write_json_mock method
            self.session.mock_config.write_json_mock(
                f"{mock_file_base}_{self.session.mock_config.writeMockSuffix}.json",
                {}
            )
            
        return True
