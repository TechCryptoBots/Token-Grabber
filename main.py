import json
from account import Account
from discord_grabber import get_discord_token
from twitter_grabber import get_twitter_tokens
from tqdm import tqdm


def load_data_from_file(filename, line_reader_function):
    print(f"Loading credentials from {filename}")
    credentials = list()
    i = 1
    with open(filename, "r") as f:
        for line in f:
            line = line.replace(" ", "").replace("\n", "")
            data = {}
            try: 
                data = line_reader_function(line)
            except Exception:
                print(f"Couldn't read line {i}")
                data["username"], data["password"] = "", ""
        
            credentials.append(data)
            i += 1
        
    return credentials


def load_accounts(discord_filename, twitter_filename, proxy_filename=""):
    credentials = list()
    
    def discord_reader_function(line):
        if line == "":
            return {"username": "", "password": ""}
        data = {}
        data["username"], data["password"] = line.split(":")
        return data
    
    discord_credentials = load_data_from_file(discord_filename, discord_reader_function)
    
    def twitter_reader_function(line):
        if len(line.split(":")) == 2:
            return {"username": line.split(":")[0], "password": line.split(":")[1]}
        elif len(line.split(":")) >= 3:
            return {"username": line.split(":")[0], "password": line.split(":")[1], "phone": line.split(":")[2]}
        else:
            return {"username": "", "password": ""}
        
    twitter_credentials = load_data_from_file(twitter_filename, twitter_reader_function)
    proxies = []
    if proxy_filename != "":
        proxies = load_data_from_file(proxy_filename, lambda line: line)
    for i in range(max(len(discord_credentials), len(twitter_credentials))):
        account = {}
        
        if i < len(discord_credentials): 
            account["discord"] = discord_credentials[i]

        if i < len(twitter_credentials):
            account["twitter"] = twitter_credentials[i]
        
        if i < len(proxies):
            account["proxy"] = proxies[i]
        else:
            account["proxy"] = ""
        
        credentials.append(account)
    
    return credentials

def save_accounts_state(accounts):
    data = {}

    for i, account in enumerate(accounts):
        data[i] = account.to_dict()

    with open("accounts.json", "w") as file:
        json.dump(data, file, indent=4)

if __name__ == "__main__":
    
    credentials_accounts = load_accounts("discord_accounts.txt", "twitter_accounts.txt", "proxies.txt")
    accounts = []
    
    for credentials_account in tqdm(credentials_accounts):
        discord_token = get_discord_token(credentials_account["discord"], credentials_account["proxy"]) if credentials_account.get("discord") else ""
        twitter_auth_token, twitter_access_token = get_twitter_tokens(credentials_account["twitter"], credentials_account["proxy"]) if credentials_account.get("twitter") else ("", "")
        
        account = Account()
        account.discord_token = discord_token if discord_token else ""
        account.twitter_token = twitter_auth_token if twitter_auth_token else ""
        account.twitter_access_token = twitter_access_token if twitter_access_token else ""
        account.proxy = credentials_account["proxy"]
        accounts.append(account)
        
        save_accounts_state(accounts)
        
        
        
    