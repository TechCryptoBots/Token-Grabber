# Token Grabber (by @nomorehumor and @tech_crypt0)
This is auth token grabber for twitter and discord accounts.
To use it, simply put the following data in following files:
- In `discord_accounts.txt`: put discord accounts in format `username:password` line-by-line
- In `twitter_accounts.txt`: put twitter accounts in format `username:password:phone` (phone is optional, if not linked put just `username:password`) line-by-line
- (optional) In `proxies.txt`: put proxies in format `type://username:password@ip:port` line-by-line

You can also fill out only discord or only twitter accounts, in this case the bot will grab tokens only for given accounts.

To launch you need Python 3.9+

Before launching switch to the bot folder in console and run:
```
pip install -r requirements.txt
```

After that run in console:
```
python main.py
```

The bot will output `accounts.json`. It contains tokens and more other blank parameters for each account in JSON format. The file can be loaded directly to our Gleam Bot that automates the filling of gleam forms. If you are interested contact @dmdeth in Telegram

# Warning regarding Discord accounts
There is a problem with Discord accounts because of ip-check from Discord. If you want to retrieve tokens for Discord accounts, you have to login at least once from your IP (or from proxy IP, if you use proxy). Discord sends confirmation link to your email and bot can't deal with it right now, but probably will be in the future (if anybody wants to contribute on this, you are welcome)

# Troubleshooting
If yout have any problems with the script, visit our Telegram Channel @tech_crypt0 for FAQ or contact @dmdeth in telegram directly

# Contribution
Feel free to open an issue or ready PR to this project. Our team builds more bots for social media abusing/automatization, especially in context of Crypto/Web3 projects. If you are interested, visit our Telegram channel: @tech_crypt0 or contact @dmdeth in telegram.
