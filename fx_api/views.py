from fx_api import app
from flask import jsonify, abort, make_response, render_template, request
from .models import xrs


# Website help page
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', title='Help')


# Get all exchange rates
@app.route('/api/v1/xrs', methods=['GET'])
def get_xrs():
    return jsonify({'xrs': xrs})


# Get single exchange rate
@app.route('/api/v1/xrs/<string:xrcode>')
def get_xr(xrcode):
    capture = [xr for xr in xrs if xr['xrcode'] == xrcode.upper()]
    if len(capture) is 0:
        abort(404)
    return jsonify({'xr': capture[0]})


# Convert currency
@app.route('/api/v1/xrs/<string:rate1>/<string:rate2>/<value>', methods=['GET'])
def get_conversion(rate1, rate2, value):
    try:
        value = float(value)
    except ValueError:
        abort(make_response(jsonify(Error="Exchange value is not float or int"), 400))

    xrconv = _collect_rates(rate1, rate2)

    if not xrconv["from"] or not xrconv["to"]:
        abort(make_response(jsonify(Error="One or more rates not found - "
                                          "{0}:{1}  {2}:{3}"
                                    .format(rate1.upper(), xrconv["from"], rate2.upper(), xrconv["to"])), 400))
    if 'fee' in request.args:
        value = _levy_fee(xrconv["from"], value)

    return jsonify(conversion=round(_convert(value, xrconv["from"], xrconv["to"]), 2))


def _convert(value, xrfrom, xrto):
    """Currency conversion
        Args:
            value (float): amount to be converted
            xrfrom (float): initial currency rate
            xrto (float): final currency rate
        Returns:
            converted amount
    """
    return value*xrto/xrfrom


def _levy_fee(xrfrom, value):
    """If the source amount < 1000 GBP, levy 25 pound fix fee. For source amount >=1000 GBP apply 1% fee.
        Args:
            xrfrom (float/int): initial currency rate
            value (float): amount to be converted
        Returns:
            fee adjusted amount for conversion
    """
    if float(xrfrom) != 1.0:
        value = _convert(value, xrfrom, 1.0)

    if value < 1000.0:
        value -= 25.0
    else:
        value -= value*0.01

    return value if float(xrfrom) == 1.0 else _convert(value, 1.0, xrfrom)


def _collect_rates(rate1, rate2, xrconv=None):
    """search through list of rates in xrs for rate1 and rate2
        Args:
            rate1 (string): exchagne rate code (initial currency)
            rate2 (string): exchange rate code (final currency)
        Returns:
            dictionary of corresponding rates
    """
    if not xrconv:
        xrconv = {"from": None, "to": None}
    assert "from" in xrconv and "to" in xrconv, "No from or to keys in xrconv dict"

    for xr in xrs:
        isfrom = xr['xrcode'] == rate1.upper()
        isto = xr['xrcode'] == rate2.upper()

        if isfrom and isto:
            xrconv["from"] = xr['rate']
            xrconv["to"] = xr['rate']
        elif isfrom:
            xrconv["from"] = xr['rate']
        elif isto:
            xrconv["to"] = xr['rate']
        else:
            continue
    return xrconv


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify(error="Not found"), 404)
