import json
import requests

def get_discord_token(account, proxy=""):
    if account["username"] == "" or account["password"] == "":
        return ""
    
    data = {
        "login": account["username"],
        "password": account["password"],
    }
        
    headers = {
        "content-type": "application/json"
    }
        
    r = requests.post("https://discord.com/api/v9/auth/login", headers=headers, data=json.dumps(data), proxies={"http": proxy})
    if r.status_code == 200:
        json_response = r.json()
        token = json_response["token"]
        return token
    else:
        print(f"\nError during getting discord token for account {account}")
        return ""


