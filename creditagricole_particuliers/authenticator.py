from urllib import parse
import requests
import json
import os

from creditagricole_particuliers import regionalbanks
from creditagricole_particuliers.mockconfig import MockConfig


class Authenticator:
    def __init__(self, username, password, department, mock_config=None):
        """
        Initialize authenticator and perform authentication
        
        Args:
            username (str): User's login username
            password (list[int]): User's login password as array of digits
            department (int): User's department code
            mock_config (MockConfig, optional): Mock configuration. Defaults to None.
        """
        self.url = "https://www.credit-agricole.fr"
        self.ssl_verify = True
        
        # Set mock configuration
        if mock_config is None:
            self.mock_config = MockConfig()
        else:
            self.mock_config = mock_config
            
        self.username = username
        self.password = password
        self.department = department
        self.regional_bank_url = "ca-undefined"
        self.cookies = None

        self.find_regional_bank()
        self.authenticate()

    def find_regional_bank(self, use_local=True):
        """
        Finds regional bank URL
        
        Args:
            use_local (bool): Uses local aliases.json if True, otherwise calls the API. Defaults to True.
            
        Raises:
            Exception: If regionalBankUrlPrefix is missing
        """
        if use_local:
            filepath = os.path.join(os.path.dirname(__file__), r"aliases.json")
            with open(filepath, "r") as f:
                aliases = json.load(f)

            self.regional_bank_url = aliases[str(self.department).zfill(2)]["alias"]

        else:
            # Pass the MockConfig to RegionalBanks
            regional_bank = regionalbanks.RegionalBanks(mock_config=self.mock_config).by_departement(department=self.department)
            if "regionalBankUrlPrefix" not in regional_bank:
                raise Exception("[error] regionalBankUrlPrefix key is missing")

            self.regional_bank_url = regional_bank["regionalBankUrlPrefix"][1:-1]

    def map_digit(self, key_layout, digit):
        """map digit with key layout"""
        i = 0
        for k in key_layout:
            if int(digit) == int(k):
                return i
            i += 1

    def authenticate(self):
        """
        Performs authentication process
        
        Raises:
            Exception: If authentication fails due to invalid credentials or server errors
        """

        mock_file_keypad_base = "authentication_keypad"
        
        if self.useMocks:
            # Use mock data for keypad
            data = self.mock_config.read_json_mock(f"{mock_file_keypad_base}_{self.mock_config.useMockSuffix}.json")
            # Create a mock response with cookies
            r = type('obj', (object,), {
                'cookies': requests.cookies.RequestsCookieJar(),
                'status_code': 200,
                'text': data
            })
        else:
            # get the keypad layout for the password
            url = "%s/%s/particulier/" % (self.url, self.regional_bank_url)
            url += "acceder-a-mes-comptes.authenticationKeypad.json"
            r = requests.post(url=url,
                            verify=self.ssl_verify)
            if r.status_code != 200:
                raise Exception("[error] keypad: %s - %s" % (r.status_code, r.text))
            data = r.text
            
        # Write mock data if requested
        if self.writeMocks:
            self.mock_config.write_json_mock(f"{mock_file_keypad_base}_{self.mock_config.writeMockSuffix}.json", data)

        self.cookies = r.cookies
        rsp = json.loads(data)
        self.keypadId = rsp["keypadId"]

        # compute the password according to the layout
        j_password = []
        for d in self.password:
            k = self.map_digit(key_layout=rsp["keyLayout"], digit=d)
            j_password.append("%s" % k)

        # authenticate the user
        mock_file_auth_base = "authentication_security"
        
        if self.useMocks:
            # Use mock data for authentication
            cookies_json_string = self.mock_config.read_json_mock(f"{mock_file_auth_base}_{self.mock_config.useMockSuffix}.json")
            cookies_dict = json.loads(cookies_json_string)
            hydrated_cookies = requests.cookies.cookiejar_from_dict(cookies_dict)
            # Create a mock response with cookies
            r2 = type('obj', (object,), {
                'cookies': hydrated_cookies,
                'status_code': 200,
                'text': "{}" # Set a dummy JSON text as r2.text is not used for auth mock
            })
        else:
            # get the keypad layout for the password
            url = "%s/%s/particulier/" % (self.url, self.regional_bank_url)
            url += "acceder-a-mes-comptes.html/j_security_check"
            headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
            payload = {'j_password': ",".join(j_password),
                      'path': '/content/npc/start',
                      'j_path_ressource': '%%2F%s%%2Fparticulier%%2Foperations%%2Fsynthese.html' % self.regional_bank_url,
                      'j_username': self.username,
                      'keypadId': rsp["keypadId"],
                      'j_validate': "true"}
            r2 = requests.post(url=url,
                              data=parse.urlencode(payload),
                              headers=headers,
                              verify=self.ssl_verify,
                              cookies=r.cookies)
            if r2.status_code != 200:
                raise Exception("[error] securitycheck: %s - %s" % (r2.status_code, r2.text))
                
            # Write mock data
            cookies_dict = r2.cookies.get_dict()
            cookies_json_string = json.dumps(cookies_dict)
        
        self.mock_config.write_json_mock(f"{mock_file_auth_base}_{self.mock_config.writeMockSuffix}.json", cookies_json_string)

        # success, extract cookies and save-it
        self.cookies = requests.cookies.merge_cookies(self.cookies, r2.cookies)

    @property
    def useMocks(self):
        """Property accessor for mock_config.useMocks"""
        return self.mock_config.useMocks()

    @property
    def writeMocks(self):
        """Property accessor for mock_config.writeMocks"""
        return self.mock_config.writeMocks()
