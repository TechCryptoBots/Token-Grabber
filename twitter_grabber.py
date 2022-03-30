from click import password_option
from requests_oauthlib import OAuth1Session
import requests
import sys
from seleniumwire.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException

CONSUMER_KEY = "usEig2joNLSMsFP8gYsH8SExY"
CONSUMER_SECRET = "PTkxtqzZB9mdT8OccIrs2Dh7zOtI8CQyAqyyLid7axQtASxGGB"

# Request an OAuth Request Token. This is the first step of the 3-legged OAuth flow. This generates a token that you can use to request user authorization for access.
def request_token(proxy=""):

    oauth = OAuth1Session(CONSUMER_KEY, client_secret=CONSUMER_SECRET, callback_uri='oob')
    oauth.proxies = {'all': proxy}

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

def get_user_access_tokens(resource_owner_oauth_token, resource_owner_oauth_token_secret, authorization_pin, proxy=""):

    oauth = OAuth1Session(CONSUMER_KEY, 
                            client_secret=CONSUMER_SECRET, 
                            resource_owner_key=resource_owner_oauth_token, 
                            resource_owner_secret=resource_owner_oauth_token_secret, 
                            verifier=authorization_pin)
    oauth.proxies = {'all': proxy}
    
    url = "https://api.twitter.com/oauth/access_token"

    response = oauth.fetch_access_token(url)
    access_token = response['oauth_token']
    access_token_secret = response['oauth_token_secret']
    user_id = response['user_id']
    screen_name = response['screen_name']

    return(access_token, access_token_secret, user_id, screen_name)

def get_webdriver(proxy=""):
    options = ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('window-size=1920x1080')    
    options.add_argument("--log-level=3")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    wire_options = dict()
    if proxy != "":
        wire_options["proxy"] = {
            "http": proxy,
            'no_proxy': 'localhost,127.0.0.1' # excludes
        }
    
    driver = Chrome(options=options, seleniumwire_options=wire_options)
    return driver

def get_authorization_token_and_pin(authorization_url: str, account: dict, proxy=""):
    driver = get_webdriver(proxy)
    driver.get(authorization_url)
    
    # Authorize with credentials
    auth_form = driver.find_element(By.TAG_NAME, "form")
    
    username_input = auth_form.find_element(By.ID, "username_or_email")
    driver.execute_script("arguments[0].value=\"" + account["username"] + "\";", username_input)

    password_input = auth_form.find_element(By.ID, "password")
    driver.execute_script("arguments[0].value=\"" + account["password"] + "\";", password_input)

    auth_form.submit()
    
    challenge_forms = driver.find_elements(By.ID, "login-challenge-form")
    if len(challenge_forms) > 0:
        challenge_form = challenge_forms[0]
        phone_number_field = challenge_form.find_element(By.ID, "challenge_response")
        driver.execute_script("arguments[0].value=\"" + account["phone"] + "\";", phone_number_field)
        challenge_form.submit()
        
    pin = ""
    try:
        code_element = driver.find_element(By.TAG_NAME, "code")
        pin = code_element.text
    except Exception:
        print("\nCouldn't retrieve twitter access token")
        
    auth_token = driver.get_cookie("auth_token")["value"]
    return auth_token, pin

def get_twitter_tokens(account: dict, proxy=""):
    if account["username"] == "" or account["password"] == "":
        return "", ""
    
    try:
        resource_owner_oauth_token, resource_owner_oauth_token_secret = request_token(proxy=proxy)
        authorization_url = get_user_authorization_url(resource_owner_oauth_token)
        auth_token, pin = get_authorization_token_and_pin(authorization_url, account, proxy=proxy)
        if pin != "":
            access_token, access_token_secret, user_id, screen_name = get_user_access_tokens(resource_owner_oauth_token, resource_owner_oauth_token_secret, pin, proxy=proxy)
            return auth_token, access_token
        else: 
            return auth_token, ""
    except Exception:
        print(f"\nError during getting twitter token for account {account}")
        return None, None
    