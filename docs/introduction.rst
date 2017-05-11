.. _introcution:

============
Introduction
============

This program provides an asyncio smtp to Slack/Mattermost webhook bridge based
on an `asyncio smtp implementation <https://aiosmtpd.readthedocs.io>`_. By
default all mails transformed into messages are send to the default channel
configured by the webhook. If mail is formatted as html, it will by default try to convert it to a Markdown formatted text using `html2text <http://alir3z4.github.io/html2text/>`_.

Il is mainly designed to be run as a :doc:`docker service container <docker>`.

This program provides a way to filter mails using `sieve <http://sieve.info/>`_
compatible language to discard messages or send them to a different channel or
user. You can check examples in the :doc:`sieve documentation page <sieve>`.

**NB**: If you plan to host an instance, please check the :doc:`security
considerations <security>`_
**NB2**: Slack or Mattermost webhooks can't be used to send a private message to
the user who configured the webhook. We advise to configure the sieve filter to
prevent sending messages to this user or create a webhook with a dedicated user.

Similar tools
=============

`email-actions <https://github.com/shantanugoel/email-actions>`_ : A more 
generic tool using `aiosmtpd <https://aiosmtpd.readthedocs.io>`_  to trigger
actions.
