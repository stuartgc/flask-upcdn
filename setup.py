"""
Flask-CDN
---------

Serve the static files in your Flask app from a CDN.
"""
from setuptools import setup


setup(
    name='Flask-UPCDN',
    version='1.2.1',
    url='https://github.com/Hearst-DD/flask-cdn.git',
    license='MIT',
    author='William Fagan',
    author_email='will@wichitacode.com',
    description='Serve the static files in your Flask app from a CDN.',
    long_description=__doc__,
    py_modules=['flask_upcdn'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask'
    ],
    test_suite='tests',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
