from json.encoder import py_encode_basestring_ascii
import requests
import json
import os

from creditagricole_particuliers import operations
from creditagricole_particuliers import accounts

class Card:
    def __init__(self, session, card):
        """
        Initialize Card
        
        Args:
            session (Authenticator): Authentication session
            card (dict): Card data
        """
        self.session = session
        self.card = card
        self.idCompte = card["idCompte"]
        self.typeCarte = card["typeCarte"]
        self.idCarte = card["idCarte"]
        self.titulaire = card["titulaire"]
        
    def __str__(self):
        """str"""
        return f"Carte[compte={self.idCompte}, type={self.typeCarte}, titulaire={self.titulaire}]"

    def get_operations(self):
        """
        Get deferred operations for this card
        
        Returns:
            DeferredOperations: Card deferred operations
        """
        account = accounts.Accounts(session=self.session).search(num=self.idCompte)

        return operations.DeferredOperations(session=self.session, 
                                             compteIdx=account.compteIdx,
                                             grandeFamilleCode=account.grandeFamilleCode,
                                             carteIdx=self.card["index"])

    def as_json(self):
        """return as json"""
        return json.dumps(self.card)

class Cards:
    def __init__(self, session):
        """
        Initialize Cards collection
        
        Args:
            session (Authenticator): Authentication session
        """
        self.session = session
        self.cards_list = []

        self.get_cards_per_account()

    def __len__(self):
        """Return the number of operations"""
        return len(self.cards_list)

    def __iter__(self):
        """iter"""
        self.n = 0
        return self

    def __next__(self):
        """next"""
        if self.n < len(self.cards_list):
            op = self.cards_list[self.n]
            self.n += 1
            return op
        else:
            raise StopIteration

    def as_json(self):
        """as json"""
        _accs = []
        for acc in self.cards_list:
            _accs.append(acc.card)
        return json.dumps(_accs)

    def search(self, num_last_digits):
        """search card """
        for cb in self.cards_list:
            if cb.idCarte.endswith(num_last_digits):
                return cb
        raise Exception( "[error] card not found" )

    def get_cards_per_account(self):
        """
        Retrieves cards from the bank API
        
        Raises:
            Exception: If the API request fails
        """
        mock_file_base = "cards"
        
        if self.session.useMocks:
            # Use the new read_json_mock method to get raw content
            data = self.session.mock_config.read_json_mock(f"{mock_file_base}_{self.session.mock_config.useMockSuffix}.json")
        else:
            # call cards resources
            url = "%s" % self.session.url
            url += "/%s/particulier/operations/" % self.session.regional_bank_url
            url += "moyens-paiement/gestion-carte-v2/mes-cartes/jcr:content.listeCartesParCompte.json"
            r = requests.get(url=url, verify=self.session.ssl_verify, cookies=self.session.cookies)
            if r.status_code != 200:
                raise Exception( "[error] get cards: %s - %s" % (r.status_code, r.text) )
            
            data = r.text
            
        # Write mock data if requested
        if self.session.writeMocks:
            self.session.mock_config.write_json_mock(f"{mock_file_base}_{self.session.mock_config.writeMockSuffix}.json", data)

        r = json.loads(data)
        if "comptes" not in r:
            raise Exception("[error] compte not found in response ")

        for account in r["comptes"]:
            for card in account["listeCartes"]:
                card["idCompte"] = account["idCompte"]
                self.cards_list.append(Card(self.session, card))
