from re import M
import requests
import json
from account import Account
from discord_grabber import get_discord_token
from twitter_grabber import get_twitter_tokens
from tqdm import tqdm

def load_credentials_from_file(filename):
    credentials = list()
    i = 1
    with open(filename, "r") as f:
        line = f.readline().replace(" ", "")
        data = {}
        try: 
            data["username"], data["password"] = line.split(":")
            credentials.append(data)
        except Exception:
            print(f"Couldn't read line {i}")
        i += 1
    return credentials

def load_credentials(discord_filename, twitter_filename):
    credentials = list()
    
    discord_credentials = load_credentials_from_file(discord_filename)
    twitter_credentials = load_credentials_from_file(twitter_filename)
    for i in range(max(len(discord_credentials), len(twitter_credentials))):
        account = {}
        
        if i < len(discord_credentials): 
            account["discord"] = discord_credentials[i]

        if i < len(twitter_credentials):
            account["twitter"] = twitter_credentials[i]
        
        credentials.append(account)
    
    return credentials

def save_accounts_state(accounts):
    data = {}

    for i, account in enumerate(accounts):
        data[i] = account.to_dict()

    with open("accounts.json", "w") as file:
        json.dump(data, file, indent=4)

if __name__ == "__main__":
    
    credentials_accounts = load_credentials("discord_accounts.txt", "twitter_accounts.txt")
    accounts = []
    
    for credentials_account in tqdm(credentials_accounts):
        account = Account()

        discord_token = get_discord_token(credentials_account["discord"])
        account.discord_token = discord_token if discord_token != None else ""

        twitter_auth_token, twitter_access_token = get_twitter_tokens(credentials_account)
        account.twitter_token = twitter_auth_token if twitter_auth_token != None else ""
        accounts.append(account)
        
    save_accounts_state(accounts)
        
        
        
    