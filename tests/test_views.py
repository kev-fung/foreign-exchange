import unittest
from flask import json, jsonify
from fx_api import app, models


class TestViews(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_indexhtml(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200, "failed loading index page")

    def test_getxrs(self):
        response = self.app.get('/api/v1/xrs')
        data = json.loads(response.data)
        self.assertEqual(data['xrs'], models.xrs, "failed getting xrs")

    def test_getxr(self):
        response = self.app.get('/api/v1/xrs/GBP')
        data = json.loads(response.data)
        self.assertEqual(data['xr']['rate'], 1, "failed getting single xr")

    def test_conversion(self):
        response = self.app.get('/api/v1/xrs/GBP/USD/100')
        data = json.loads(response.data)
        self.assertEqual(float(data['conversion']), float(130), "failed to convert")

    def test_conversion_fee(self):
        response = self.app.get('/api/v1/xrs/GBP/USD/100?fee')
        data = json.loads(response.data)
        self.assertEqual(float(data['conversion']), float(97.5), "failed to convert")

    def test_conv_wrongrate(self):
        response = self.app.get('/api/v1/xrs/abc/USD/100')
        self.assertEqual(response.status_code, 400)

    def test_conv_wrongamount(self):
        response = self.app.get('/api/v1/xrs/GBP/USD/10a-0')
        self.assertEqual(response.status_code, 400)

    def test_conv_wrongcases(self):
        response = self.app.get('/api/v1/xrs/gbp/UsD/100')
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
