import os

from flask import url_for as flask_url_for
from flask import current_app, request


def url_for(endpoint, **values):
    """
    Generates a URL to the given endpoint.

    If the endpoint is for a static resource then a URL to the CDN is
    generated, otherwise the call is passed on to `flask.url_for`.

    Because this function is set as a jinja environment variable when
    `CDN.init_app` is invoked, this function replaces `flask.url_for` in
    templates automatically. It is unlikely that this function will need to be
    directly called from within your application code, unless you need to refer
    to static assets outside of your templates.
    """
    app = current_app

    if app.debug:
        return flask_url_for(endpoint, **values)

    if endpoint == 'static' or endpoint.endswith('.static'):
        cdn_https = app.config['CDN_HTTPS']

        scheme = 'http'
        if cdn_https is True or (cdn_https is None and request.is_secure):
            scheme = 'https'

        static_folder = app.static_folder
        if request.blueprint is not None:
            static_folder = app.blueprints[request.blueprint].static_folder

        urls = app.url_map.bind(app.config['CDN_DOMAIN'], url_scheme=scheme)

        if app.config['CDN_TIMESTAMP']:
            tstamp = int(os.path.getmtime(path))
            path = os.path.join(tstamp, static_folder, values['filename'])
            values['t'] = tstamp

        return urls.build(endpoint, values=values, force_external=True)

    return flask_url_for(endpoint, **values)


class UPCDN(object):
    """
    The UPCDN object allows your application to use Flask-CDN.

    When initialising a CDN object you may optionally provide your
    :class:`flask.Flask` application object if it is ready. Otherwise,
    you may provide it later by using the :meth:`init_app` method.

    :param app: optional :class:`flask.Flask` application object
    :type app: :class:`flask.Flask` or None
    """
    def __init__(self, app=None):
        """
        An alternative way to pass your :class:`flask.Flask` application
        object to Flask-CDN. :meth:`init_app` also takes care of some
        default `settings`_.

        :param app: the :class:`flask.Flask` application object.
        """
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        defaults = [('CDN_DOMAIN', None),
                    ('CDN_HTTPS', None),
                    ('CDN_TIMESTAMP', True)]

        for k, v in defaults:
            app.config.setdefault(k, v)

        if app.config['CDN_DOMAIN']:
            app.jinja_env.globals['url_for'] = url_for
