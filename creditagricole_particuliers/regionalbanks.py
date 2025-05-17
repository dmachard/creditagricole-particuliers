from urllib import parse
import requests
import json
import os
from creditagricole_particuliers.mockconfig import MockConfig

class RegionalBanks:
    def __init__(self, mock_config=None):
        """
        Initialize Regional Banks manager
        
        Args:
            mock_config (MockConfig, optional): Mock configuration. Defaults to None.
        """
        # Since RegionalBanks doesn't have a session, the MockConfig can be used directly
        if mock_config is None:
            self.mock_config = MockConfig()
        else:
            self.mock_config = mock_config
            
        # The URL and SSL verification are set directly
        self.url = "https://www.credit-agricole.fr"
        self.ssl_verify = True

    def by_departement(self, department):
        """
        Get regional bank data from the Credit Agricole API by department code
        
        Args:
            department (str or int): Department code (string or integer)
            
        Returns:
            RegionalBankData: Regional bank data from the API
            
        Raises:
            Exception: If the request fails or no bank is found
        """
        mock_file_base = f"regionalbank-{department}"
        # Use mock data if configured

        if self.mock_config.useMocks():
            # Use the new read_json_mock method
            data = self.mock_config.read_json_mock(f"{mock_file_base}_{self.mock_config.useMockSuffix}.json")
        else:
            # Fetch live data
            url = "%s/particulier/acces-cr.get-cr-by-department.json" % (self.url)
            headers={'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
            payload = {'department': "%s" % department}
            r = requests.post(url=url, 
                            data=parse.urlencode(payload),
                            headers=headers,
                            verify=self.ssl_verify)
            if r.status_code != 200:
                raise Exception( "[error] get regional bank by departement: %s - %s" % (r.status_code, r.text) )
            data = r.text
            
        # Write mock data if configured
        if self.mock_config.writeMocks():
            self.mock_config.write_json_mock(f"{mock_file_base}_{self.mock_config.writeMockSuffix}.json", data)
                    
        regionalBanks = json.loads(data)

        if not len(regionalBanks):
            raise Exception( "[error] get regional bank by departement code not found"  )

        return regionalBanks[0]