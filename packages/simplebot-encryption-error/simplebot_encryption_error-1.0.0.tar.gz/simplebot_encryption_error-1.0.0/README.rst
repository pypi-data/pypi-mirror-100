Encryption Error
================

.. image:: https://img.shields.io/pypi/v/simplebot_encryption_error.svg
   :target: https://pypi.org/project/simplebot_encryption_error

.. image:: https://img.shields.io/pypi/pyversions/simplebot_encryption_error.svg
   :target: https://pypi.org/project/simplebot_encryption_error

.. image:: https://pepy.tech/badge/simplebot_encryption_error
   :target: https://pepy.tech/project/simplebot_encryption_error

.. image:: https://img.shields.io/pypi/l/simplebot_encryption_error.svg
   :target: https://pypi.org/project/simplebot_encryption_error

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black

A `SimpleBot`_ plugin that adds a filter to reply back a warning message when the bot receive a message that can't be decrypted so the user receives the bot's new public key and encryption works again.

This can happen if you change the bot's encryption key or re-create the bot account.

Install
-------

To install run::

  pip install simplebot-encryption-error


.. _SimpleBot: https://github.com/simplebot-org/simplebot
