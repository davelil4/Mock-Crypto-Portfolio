# Mock-Crypto-Wallet
This is a Plotly Dash app that is intended to work as a mock crypto wallet. It is still a work in progress, but should be completed by the end of January 2023.

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
To start up the app, run `python app.py`. Then visit http://127.0.0.1:8050/ in your web browser. The app will be running there.
