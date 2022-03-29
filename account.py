from typing import Dict, List
import hashlib

class Account:

    def __init__(self, name='', last_name='', email='', twitter_token='', discord_token='', proxy='', custom_data={}, custom_answers={}, access_token='') -> None:
        self.twitter_token = twitter_token
        self.discord_token = discord_token
        self.name = name
        self.last_name = last_name
        self.proxy = proxy
        self.email = email
        self.custom_data = custom_data
        self.custom_answers = custom_answers
        self.twitter_access_token = access_token

    def get_profile_dir(self) -> str:
        m = hashlib.sha256()
        m.update(self.twitter_token.encode('utf-8'))
        return m.hexdigest()
    
    def to_dict(self) -> Dict:
        data = {
            "name": self.name,
            "last_name": self.last_name,
            "twitter_token": self.twitter_token,
            "twitter_access_token": self.twitter_access_token,
            "proxy": self.proxy,
            "custom_data": self.custom_data,
            "custom_answers": self.custom_answers,
            "discord_token": self.discord_token,
            "email": self.email,
        }
        
        return data
    
    def __str__(self) -> str:
        return f"Account: {self.to_dict()}"

# class AccountLoader:

#     def __init__(self, accounts_file, proxy_file=None) -> None:
#         self.accounts_file = accounts_file
#         self.proxy_file = proxy_file

#     def load_accounts(self) -> List[Account]:
#         accounts_set = open(self.accounts_file, 'r',
#                            encoding='utf-8').read().splitlines()
#         account_list = []        
        
#         for i, token in zip(range(1, len(accounts_set)+1), accounts_set):
#             account_list.append(Account(i, token))
            
#         if self.proxy_file:
#             proxies = open(self.proxy_file, 'r',
#                            encoding='utf-8').read().splitlines()
            
#             for i in range(len(proxies)):
#                 account_list[i].proxy = proxies[i]
            
        

#         return account_list
