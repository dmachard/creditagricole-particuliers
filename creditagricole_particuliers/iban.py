import json
import requests
import os

class Iban:
    def __init__(self, session, compteIdx, grandeFamilleCode, numeroCompte):
        """
        Initialize IBAN fetcher
        
        Args:
            session (creditagricole_particuliers.authenticator.Authenticator): Authenticated session
            compteIdx (str): Account index
            numeroCompte (str): Account number
            grandeFamilleCode (str): Grande famille code
        """
        self.session = session
        self.compteIdx = compteIdx
        self.numeroCompte = numeroCompte
        self.grandeFamilleCode = grandeFamilleCode
        self.iban = {}
        self.ibanCode = "-"

        self.get_iban_data()

    def __str__(self):
        """stre representation"""
        return f"Iban[compte={self.numeroCompte}, code={self.ibanCode}]"

    def get_iban_data(self):
        """
        Retrieves IBAN from bank API
        
        Raises:
            Exception: If the API request fails
        """
        mock_file_base = f"account-{self.grandeFamilleCode}-{self.compteIdx}_iban"
        
        if self.session.useMocks:
            # Use the new read_json_mock method to get raw content
            data = self.session.mock_config.read_json_mock(f"{mock_file_base}_{self.session.mock_config.useMockSuffix}.json")
        else:
            url = "%s" % self.session.url
            url += "/%s/particulier/operations/" % self.session.regional_bank_url
            url += "operations-courantes/editer-rib/"
            url += "jcr:content.ibaninformation.json?compteIdx=%s&grandeFamilleCode=%s" % (self.compteIdx,self.grandeFamilleCode)
            r = requests.get(url=url, verify=self.session.ssl_verify, cookies=self.session.cookies)
            if r.status_code != 200:
                raise Exception( "[error] get_iban_data: %s - %s" % (r.status_code, r.text) )
            data = r.text
            
        # Write mock data if requested
        if self.session.writeMocks:
            self.session.mock_config.write_json_mock(f"{mock_file_base}_{self.session.mock_config.writeMockSuffix}.json", data)

        self.iban = json.loads(data)
        self.ibanCode = self.iban["ibanData"]["ibanData"]["ibanCode"]

    def as_json(self):
        """return as json"""
        return json.dumps(self.iban)