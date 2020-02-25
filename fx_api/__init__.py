from flask import Flask

app = Flask(__name__)

# flask requires import AFTER object creation - breaks circular import between views app import and fx_api
from fx_api import views
