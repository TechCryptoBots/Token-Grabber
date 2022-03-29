from click import password_option
from requests_oauthlib import OAuth1Session
import requests
import sys
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException

CONSUMER_KEY = "usEig2joNLSMsFP8gYsH8SExY"
CONSUMER_SECRET = "PTkxtqzZB9mdT8OccIrs2Dh7zOtI8CQyAqyyLid7axQtASxGGB"

# Request an OAuth Request Token. This is the first step of the 3-legged OAuth flow. This generates a token that you can use to request user authorization for access.
def request_token():

    oauth = OAuth1Session(CONSUMER_KEY, client_secret=CONSUMER_SECRET, callback_uri='oob')

    url = "https://api.twitter.com/oauth/request_token"

    try:
        response = oauth.fetch_request_token(url)
        resource_owner_oauth_token = response.get('oauth_token')
        resource_owner_oauth_token_secret = response.get('oauth_token_secret')
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(120)
    
    return resource_owner_oauth_token, resource_owner_oauth_token_secret

def get_user_authorization_url(resource_owner_oauth_token):
    authorization_url = f"https://api.twitter.com/oauth/authorize?oauth_token={resource_owner_oauth_token}"
    return authorization_url

def get_user_access_tokens(resource_owner_oauth_token, resource_owner_oauth_token_secret, authorization_pin):

    oauth = OAuth1Session(CONSUMER_KEY, 
                            client_secret=CONSUMER_SECRET, 
                            resource_owner_key=resource_owner_oauth_token, 
                            resource_owner_secret=resource_owner_oauth_token_secret, 
                            verifier=authorization_pin)
    
    url = "https://api.twitter.com/oauth/access_token"

    response = oauth.fetch_access_token(url)
    access_token = response['oauth_token']
    access_token_secret = response['oauth_token_secret']
    user_id = response['user_id']
    screen_name = response['screen_name']

    return(access_token, access_token_secret, user_id, screen_name)

def get_webdriver():
    options = ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('window-size=1920x1080')    
    driver = Chrome(options=options)
    return driver

def get_authorization_token_and_pin(authorization_url: str, account: dict):
    driver = get_webdriver()
    driver.get(authorization_url)
    
    auth_form = driver.find_element(By.TAG_NAME, "form")
    
    username_input = auth_form.find_element(By.ID, "username_or_email")
    driver.execute_script("arguments[0].value=\"" + account["twitter"]["username"] + "\";", username_input)

    password_input = auth_form.find_element(By.ID, "password")
    driver.execute_script("arguments[0].value=\"" + account["twitter"]["password"] + "\";", password_input)

    auth_form.submit()
    
    try:
        code_element = driver.find_element(By.TAG_NAME, "code")
        pin = code_element.text
    except Exception:
        print("Couldn't retrieve access token")
        
    auth_token = driver.get_cookie("auth_token")["value"]
    return auth_token, pin

def get_twitter_tokens(account: dict):
    # try:
    resource_owner_oauth_token, resource_owner_oauth_token_secret = request_token()
    authorization_url = get_user_authorization_url(resource_owner_oauth_token)
    auth_token, pin = get_authorization_token_and_pin(authorization_url, account)
    access_token, access_token_secret, user_id, screen_name = get_user_access_tokens(resource_owner_oauth_token, resource_owner_oauth_token_secret, pin)
    return auth_token, access_token
    # except Exception:
    #     print(f"Problem getting twitter token for account {account}")
    #     return None, None
    