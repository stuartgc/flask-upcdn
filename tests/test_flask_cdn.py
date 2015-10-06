from __future__ import unicode_literals

import unittest
import os

from flask import Flask, render_template_string

from flask.ext.upcdn import UPCDN


class DefaultsTest(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.testing = True

        UPCDN(self.app)

    def test_domain_default(self):
        """ Tests CDN_DOMAIN default value is correctly set. """
        self.assertEquals(self.app.config['CDN_DOMAIN'], None)

    def test_https_default(self):
        """ Tests CDN_HTTPS default value is correctly set. """
        self.assertEquals(self.app.config['CDN_HTTPS'], None)

    def test_timestamp_default(self):
        """ Tests CDN_TIMESTAMP default value is correctly set. """
        self.assertEquals(self.app.config['CDN_TIMESTAMP'], None)


class UrlTests(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.testing = True

        self.app.config['CDN_DOMAIN'] = 'mycdnname.cloudfront.net'
        self.app.config['CDN_TIMESTAMP'] = None

        @self.app.route('/<url_for_string>')
        def a(url_for_string):
            return render_template_string(url_for_string)

        @self.app.route('/')
        def b():
            return render_template_string("{{ url_for('b') }}")

    def client_get(self, ufs, secure=False):
        UPCDN(self.app)
        client = self.app.test_client()
        if secure:
            return client.get('/%s' % ufs, base_url='https://localhost')
        else:
            return client.get('/%s' % ufs)

    def test_url_for(self):
        """ Tests static endpoint correctly affects generated URLs. """
        # non static endpoint url_for in template
        self.assertEquals(self.client_get('').get_data(True), '/')

        # static endpoint url_for in template
        ufs = "{{ url_for('static', filename='bah.js') }}"
        exp = 'http://mycdnname.cloudfront.net/static/bah.js'
        self.assertEquals(self.client_get(ufs).get_data(True), exp)

    def test_url_for_debug(self):
        """ Tests app.debug correctly affects generated URLs. """
        self.app.debug = True
        ufs = "{{ url_for('static', filename='bah.js') }}"

        exp = '/static/bah.js'
        self.assertEquals(self.client_get(ufs).get_data(True), exp)

    def test_url_for_https(self):
        """ Tests CDN_HTTPS correctly affects generated URLs. """
        ufs = "{{ url_for('static', filename='bah.js') }}"

        https_exp = 'https://mycdnname.cloudfront.net/static/bah.js'
        http_exp = 'http://mycdnname.cloudfront.net/static/bah.js'

        self.app.config['CDN_HTTPS'] = True
        self.assertEquals(self.client_get(ufs, secure=True).get_data(True),
                          https_exp)
        self.assertEquals(self.client_get(ufs).get_data(True), https_exp)

        self.app.config['CDN_HTTPS'] = False
        self.assertEquals(self.client_get(ufs, secure=True).get_data(True),
                          http_exp)
        self.assertEquals(self.client_get(ufs).get_data(True), http_exp)

        self.app.config['CDN_HTTPS'] = None
        self.assertEquals(self.client_get(ufs, secure=True).get_data(True),
                          https_exp)
        self.assertEquals(self.client_get(ufs).get_data(True), http_exp)

    def test_url_for_timestamp(self):
        """ Tests CDN_TIMESTAMP correctly affects generated URLs. """
        ufs = "{{ url_for('static', filename='bah.js') }}"

        self.app.config['CDN_TIMESTAMP'] = "1234"
        path = os.path.join(self.app.static_folder, 'bah.js')
        exp = 'http://mycdnname.cloudfront.net/{0}/static/bah.js'.format(self.app.config['CDN_TIMESTAMP'])
        self.assertEquals(self.client_get(ufs).get_data(True), exp)

        self.app.config['CDN_TIMESTAMP'] = None
        exp = 'http://mycdnname.cloudfront.net/static/bah.js'
        self.assertEquals(self.client_get(ufs).get_data(True), exp)


if __name__ == '__main__':
    unittest.main()
