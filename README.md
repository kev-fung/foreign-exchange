# Currency conversions API

## About
A prototype RESTful web API for calculating exchanged amounts using Flask.
Only three rates are implemented so far (GBP, USD, EUR) given the nature of this project. 
The optional task of applying a fee to conversions is implemented.
Data formats are in JSON. More features will be added over time.

## Requirements
- flask == 1.1.1
- cURL client/requests
- Conda/Python 3

## Usage
**Flask service and API usage:**
1. Open python terminal and cd into foreign-exchange directory.
2. ``python run.py`` to start service. (Exit terminal (or CTRL+C) whenever you want to close service)
3. If flask doesnt run, you may need to ``set FLASK_APP=run.py`` or (``export FLASK_APP=run.py`` if Linux/Mac)
3. Open a separate terminal to use Curl commands for API interaction.
4. For python code integration it is recommended to use the Requests library.

**API:**

- Help/about html page (viewable in browser).
```` 
GET localhost:5000/
````
- Get all exchange rates
````
GET localhost:5000/api/v1/xrs
````
- Get single exchange rate
````
GET localhost:5000/api/v1/xrs/[exchange rate code]
````
- Get conversion of amount without fees
````
GET localhost:5000/api/v1/xrs/[xrcode to convert from]/[xrcode to convert to]/[amount]
````
- Get conversion of amount with fees
````
GET localhost:5000/api/v1/xrs/[xrcode to convert from]/[xrcode to convert to]/[amount]?fee
````

## Possible Extensions
 - Implement database (if persistant storage is requested).
 - Adjust exchange rates. (Post, put, delete)
 - Use flask_restful instead (class based implementation).
 - API key generator for authentication.
