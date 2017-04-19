m2mb - A mail to Slack/Mattermost webhook bridge
################################################

M2MB is a smtp server that doesn't send mails (!) but transfer the message to a Slack/Mattermost instance through a webhook.

By default, m2mb will send all mails to the default configured channel. You can configure another default channel in the command line (see ``--help``) or configure per-mail rules using sieve filters (see `documentation <https://m2mb.readthedocs.io>`_).

Requirements
------------

You need python 3.6 to use this program. If you can't install python 3.6 on your system, there is a Docker image available on `Docker Hub <https://hub.docker.com/r/thperret/m2mb>`_

Installing
----------

On your system
++++++++++++++

.. code:: bash

    $ git clone https://github.com/thperret/M2MB
    $ pip install --process-dependency-links .

With docker
+++++++++++

.. code:: bash

    $ docker pull thperret/m2mb

Running
-------

On your system
++++++++++++++

.. code:: bash

    $ m2mbd localhost 8225 http://mattermost_instance/hooks/randomid

With docker
+++++++++++

.. code:: bash

    $ docker run -e WEBHOOK_URL=http://mattermost-instance/hooks/randomid -p 8225:25 thperret/m2mb

For advanced use, see `documentation <https://m2mb.readthedocs.io>`_.
