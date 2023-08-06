============
Introduction
============

.. image:: https://codecov.io/gh/hjpotter92/sqspy/branch/master/graph/badge.svg?token=6XLSO7NPF9
   :target: https://codecov.io/gh/hjpotter92/sqspy
   :alt: Code coverage
.. image:: https://pyup.io/repos/github/hjpotter92/sqspy/shield.svg
   :target: https://pyup.io/repos/github/hjpotter92/sqspy/
   :alt: Updates
.. image:: https://readthedocs.org/projects/sqspy/badge/?version=latest
   :target: https://sqspy.docs.hjpotter92.tech/en/latest/?badge=latest
   :alt: Documentation Status
.. image:: https://travis-ci.com/hjpotter92/sqspy.svg?branch=master
   :target: https://travis-ci.com/hjpotter92/sqspy
   :alt: Build status
.. image:: https://img.shields.io/lgtm/grade/python/g/hjpotter92/sqspy.svg?logo=lgtm&logoWidth=18
   :target: https://lgtm.com/projects/g/hjpotter92/sqspy/context:python
   :alt: Language grade:: Python

A more pythonic approach to SQS producer/consumer utilities. Heavily
inspired from the `the pySqsListener
<https://pypi.org/project/pySqsListener/>`_ package.

Install
=======

.. code-block:: shell

   pip install sqspy

Usage
=====

.. code-block:: python

   from sqspy import Consumer

   class MyWorker(Consumer):
       def handle_message(self, body, attributes, message_attributes):
           print(body)

   listener = MyWorker('Q1', error_queue='EQ1')
   listener.listen()

More documentation coming soon.

Why
===

The mentioned project had a few issues which I faced while trying to
implement at my organisation. The local environment testing setup was
very flaky. The signatures for ``sqs_listener`` and ``sqs_producer``
were very different from each other.

This rewrite supports **python 3.6+ versions only**, and makes use of
a lot of newer python features. It also makes use of service resources
(for lazy calls) from the boto3 library instead of making calls via
the low level client.
