.. _m2mb:

======================================
The M2MBServer and M2MBHandler classes
======================================

The core os this module are the ``M2MBServer`` and ``M2MBHandler`` classes.

The ``M2MBServer`` class inheritates from the ``SMTP`` class of the ``aiosmtpd``
module requiring a ``webhook_url`` and optionally loads a file containing
:doc:`sieve <sieve>` rules.
You can also provide a ``default_channel`` which will be used if no rules match
or are provided, a ``username`` which will overwrite [1]_ the displayed name in
message send and a ``icon_url`` parameter which will overwrite [1]_ the displayed
icon in message send.

The ``M2MBHandler`` class inheritates from the ``AsyncMessage`` class of the
``aiosmtpd`` module which provides asynchronous called of messages handling.
``M2MBHandler`` implements a dummy ``AUTH`` command which will *always* succeed
(do not rely on it for :doc:`security <security>`) and handle message by
tranforming the mail subject as a little markdown title and the mail body as the
message send into the channel.

.. [1] If allowed by Slack/Mattermost configuration, see related documentation
