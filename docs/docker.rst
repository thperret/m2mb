.. _docker:

================
Docker container
================

A docker container is available on `Docker Hub
<https://hub.docker.com/r/thperret/m2mb/>`_.
You can run the container with the following command:

.. code:: bash

    $ docker run -e WEBHOOK_URL=http://mattermost/hooks/abcdef thperret/m2mb

It is mainly designed to run with docker-compose (see `Examples`_)

Options
=======

Environment variables
+++++++++++++++++++++

``WEBHOOK_URL``
    **required**
    the Slack/Mattermost compatible webhook url to which send the messages

``DEFAULT_CHANNEL``
    default channel to send messages to
    *defaults to webhook defined channel*

``USERNAME`` [1]_
    displayed username on messages
    *defaults to the username who created the webhook*

``ICON_URL`` [1]_
    url used to displayed icon on messages
    *defaults to Slack/Mattermost default webhook icon*

.. [1] Username and icon overwrite must be allowed by Slack/Mattermost
    configuration

Volume definition
+++++++++++++++++

Use the docker volume option to define the sieve rules file:

.. code:: bash

    $ docker run -v /path/to/local/rules.sieve:/rules.sieve thperret/m2mb

Bind port to hsoting machine
++++++++++++++++++++++++++++

You can also bind the container port serving the M2MB server to the hosting
machine:

.. code:: bash

    $ docker run -p 8225:25 thperret/m2mb

Examples
========

To run directly the container you can issue:

.. code:: bash

    $ docker run -e WEBHOOK_URL=http://mattermost/hooks/abcdef -e USERNAME=M2MB
    -e ICON_URL=http://mattermost/icon.png -e DEFAULT_CHANNEL=m2mb -v
    /srv/m2mb/rules.sieve:/rules.sieve -p 8225:25 thperret/m2mb

To configure it in a docker compose environment to be used with another app, you
can adapt the following ``docker-compose.yml`` file:

.. code:: yaml

    db:
      image: 'mariadb:10.1.22'
      container_name: 'timeoff_db'
      restart: unless-stopped
      volumes:
        - ./db:/var/lib/mysql
      environment:
        - MYSQL_ROOT_PASSWORD=root-passwd
        - MYSQL_DATABASE=timeoff
        - MYSQL_USER=timeoff
        - MYSQL_PASSWORD=timeoff-passwd

    app:
      image: thperret/timeoff-management
      container_name: 'timeoff_app'
      links:
        - db:db
          m2mb:m2mb
      restart: unless-stopped
      volumes:
        - ./config:/opt/timeoff-management/config
      ports:
        - '8088:3000'
      environment:
        - NODE_ENV=production
        - MYSQL_HOST=db
        - MYSQL_USER=timeoff
        - MYSQL_DATABASE=timeoff
        - MYSQL_PASSWORD=timeoff-passwd
        - SENDER_MAIL=timeoff@example.org
        - SMTP_HOST=m2mb
        - SMTP_PORT=25
        - SMTP_USER=none
        - SMTP_PASSWORD=none

    m2mb:
      image: thperret/m2mb
      container_name: timeoff_m2mb
      volumes:
        - ./rules.sieve:/rules.sieve
      environment:
        - WEBHOOK_URL=https://mattermost.example.org/hooks/abcdefghiklm
        - DEFAULT_CHANNEL=timeoff
        - USERNAME=timeoff
        - ICON_URL=https://icon.example.org/timeoff-icon.png
      
