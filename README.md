# Mock-Crypto-Wallet
This is a Plotly Dash app that is intended to work as a mock crypto wallet/exchange. The exchange data is from the Binance exchange, accessed via the CCTX public API. You can also access the app via crypto-wallet.herokuapp.com.

## Setting up the repository
First, you must set up the virtual environment. This is not included in the repo because it will be different depending on your system. If you would like to make changes to the app and wish to debug it, use Python 3.8. There is currently an issue when running this app on 3.11 with frozen modules, so debugging will not work.

### Windows Users:
```
python3 virtualenv -p /path/to/any/bin/python venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Mac/Linux Users:
```
virtualenv -p /path/to/any/bin/python venv
source venv/bin/activate
pip install -r requirements.txt
```

## Starting up the app

### Regular
To start up the app, run `python app.py`. Then visit http://0.0.0.0:8050/ in your web browser.

### Docker
You can also run this app with docker. If you have docker installed, run `docker-compose up` while in the repository's directory. The app will be running on 0.0.0.0:8050. If you are doing it this way, make sure to either delete the dockerfile.prod (used only for production) or specify you are using the regular dockerfile in the docker-compose.yml file.
