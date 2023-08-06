================
ta-bitwarden-cli
================


.. image:: https://img.shields.io/pypi/v/ta_bitwarden_cli.svg
        :target: https://pypi.python.org/pypi/ta_bitwarden_cli

.. image:: https://img.shields.io/travis/macejiko/ta_bitwarden_cli.svg
        :target: https://travis-ci.com/macejiko/ta_bitwarden_cli

.. image:: https://readthedocs.org/projects/ta-bitwarden-cli/badge/?version=latest
        :target: https://ta-bitwarden-cli.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status

|

Thoughtful Automation BitWarden CLI installation package

|

Installation
------------

.. warning::  For correct work please use python virtualenv approach!

::

   python3 -m virtualenv venv
   source venv/bin/activate
   pip install ta-bitwarden-cli

Code above will additionally install **bw** CLI binary to a first available folder in the $PATH

|

Example Usage
-------------

.. code:: python

        import os
        from ta_bitwarden_cli import ta_bitwarden_cli as ta

        bitwarden_credentials = {
            "username": os.getenv("BITWARDEN_USERNAME"),
            "password": os.getenv("BITWARDEN_PASSWORD"),
        }
        creds = {
            "my_vault_item": "Google Maps API Key",
        }
        bw = ta.Bitwarden(bitwarden_credentials)
        assert bw.get_credentials(creds)["my_vault_item"]["password"] == "XXXXXXX"

|

Package Testing
---------------

::

   python3 -m virtualenv venv
   source venv/bin/activate
   pip install -r requirements.txt
   BITWARDEN_USERNAME=XXX BITWARDEN_PASSWORD=YYY pytest



