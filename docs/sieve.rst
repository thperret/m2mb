.. _sieve:

=============
Sieve filters
=============

Mails can be redirect to specific channels or users by using `sieve
<http://sieve.info>`_ filtering language.
If you want to send the message to a specific channel (even a private channel),
use the ``fileinto`` sieve command, if you want to redirect the message to a
specific user, use the ``redirect`` sieve command. You can also silently discard
the mail by using the ``discard`` sieve command.

**NB**: if no rules match the mail, the default command is to ``keep`` the mail
which will be send to the ``default_channel``.
**NB2**: channels must be lower case, without non-ascii characters (remove them
if any) and spaces replaced by hyphens ``-``.
**NB3**: sieve standard requires that files are in dos specification ending
lines (``CRLF`` or ``\r\r``). For information, Mac ending lines are ``CR`` (or
``\r``) and unix ending lines are ``LF`` (or ``\n``).

Commands
========

``keep``
++++++++

In ``m2mb`` the ``keep`` command means to send the message to the default
channel.

In sieve standard, there is an implicit ``keep`` which will apply if no rules
match. 
You can also explicitly use the ``keep`` command to say that you want these
mails to be send to the default channel.

``fileinto``
++++++++++++

In ``m2mb`` the ``fileinto`` command is used to send the message to a specidig
channel. The channel *must* exists (or the sending will silently fail).

``redirect``
++++++++++++

In ``m2mb`` the ``redirect`` command is used to send the message to a specific
user. You can provide the username with or without the leading ``@``.

``stop``
++++++++

The ``stop`` command will stop further processing of the sieve rules. Can be
useful to explicitly stop processing of rules after a ``discard``, ``redirect``
or ``fileinto`` statement.

Examples
========

Exemple 1
+++++++++

The following example will send all mails containing the word ``private`` in
their subject field into the ``private`` channel. If the mail does *not*
contains the word ``private`` in the subject the filter test if the mail is
destinated to a mail address containing ``user1`` or ``user2`` and will send a
direct message to the corresponding user. If none of the previous rules match,
the message will be send to the default channel.

.. code:: sieve

    require "fileinto";

	if header :contains "Subject" ["private"] {
		fileinto "private";
		stop;
	} else {
		if address :contains "To" "user1" {
			redirect "user1";
		} elsif address :contains "To" "user2" {
			redirect "@user2";
		}
	}

Example 2
+++++++++

If you want to discard non matching mails, you can add a ``discard`` statement
at the end of the file. You should also add ``stop`` statements after all other
commands otherwise the ``discard`` statement will also be interpreted (this has
an undefined behaviour in this implementation).

.. code:: sieve

    require "fileinto";

	if header :contains "Subject" ["private"] {
		fileinto "private";
		stop;
	} else {
		if address :contains "To" "user1" {
			redirect "user1";
            stop;
		} elsif address :contains "To" "user2" {
			redirect "@user2";
            stop;
		}
	}
    discard;
