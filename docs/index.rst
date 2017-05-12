.. M2MB documentation master file, created by
   sphinx-quickstart on Tue Apr 18 15:55:18 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

================================================
m2mb - A mail to Slack/Mattermost webhook bridge
================================================

Mail To Mattermost Bridge (M2MB) is a smtp server that transform mail to a
Slack/Mattermost webhook message channel. It was mainly designed as a docker
container app to serve as smtp server for some dockerized services that we use
in our office. As mail server are hard to configure and maintain, we wanted a
tool that allowed us to recieve mails without to much hassle.

.. toctree::
    :maxdepth: 2
    :caption: Contents:

    introduction
    m2mb
    cli
    sieve
    security
    docker
    LICENSE
    
.. include::
    ../NEWS.rst


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
