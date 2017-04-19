# -*- coding: utf-8 -*-
"""
This file is part of m2mb.

m2mb is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Foobar is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
"""

import asyncio
import email
import logging

from aiosmtpd.smtp import SMTP, DATA_SIZE_DEFAULT
from aiosmtpd.handlers import AsyncMessage

import sifter.parser

from m2mb.utils import (evaluate_message, send_to_mattermost, format_mail,
                        M2MBException)


log = logging.getLogger(__name__)


class M2MBHandler(AsyncMessage):
    def __init__(self, message_class=None, *, loop=None):
        super().__init__(message_class=message_class, loop=loop)

    async def handle_AUTH(self, server, session, envelope, args):
        return "235 Authentication successful"

    async def handle_DATA(self, server, session, envelope):
        message = self.prepare_message(session, envelope)
        log.debug("message prepared")
        send, channel = await evaluate_message(server.loop,
                                               message,
                                               server.rules,
                                               server.default_channel)
        log.debug(f"send: {send}, channel: {channel}")
        if send:
            text = await format_mail(server.loop, message)
            await server.loop.run_in_executor(None, send_to_mattermost,
                    server.webhook_url, text, channel, server.username,
                    server.icon_url)
        return "250 OK"


class M2MBServer(SMTP):
    def __init__(self,
                 webhook_url,
                 hostname=None,
                 tls_context=None,
                 require_starttls=False,
                 auth_require_tls=False,
                 auth_method=lambda login, password: False,  # pragma: nocover
                 auth_required=False,
                 loop=None,
                 default_channel=None,
                 username=None,
                 icon_url=None,
                 sieve_file=None):
        super().__init__(handler=M2MBHandler(),
                       data_size_limit=DATA_SIZE_DEFAULT,
                       enable_SMTPUTF8=False,
                       decode_data=True,
                       hostname=hostname,
                       tls_context=tls_context,
                       require_starttls=require_starttls,
                       auth_require_tls=auth_require_tls,
                       auth_method=auth_method,
                       auth_required=auth_required,
                       loop=loop)
        self.webhook_url = webhook_url
        self.default_channel = default_channel
        self.username = username
        self.icon_url = icon_url
        self.rules = None

        if sieve_file:
            with open(sieve_file, newline="\r\n") as sfile:
                self.rules = sifter.parser.parse_file(sfile)


#  class M2MBChannel(SMTPChannel):
    #  """Implements AUTH command."""

    #  def __init__(self, server, conn, addr, data_size_limit=33554432, map=None,
                 #  enable_SMTPUTF8=False, decode_data=False, auth_file=None):
        #  super().__init__(server, conn, addr, data_size_limit=33554432, map=None,
                         #  enable_SMTPUTF8=False, decode_data=False)
        #  self.auth_file = auth_file

    #  def smtp_AUTH(self, arg):
        #  """smtp AUTH implementation.

        #  For now this will always succeed."""
        #  if self.auth_file is None:
            #  self.push("235 Authentication successful.")


#  class M2MBServer(SMTPServer):
    #  """SMTP server class for bridge to Slack/Mattermost incoming webhook."""

    #  channel_class = M2MBChannel

    #  def __init__(self, localaddr, remoteaddr, webhook_url,
                 #  data_size_limit=33554432, map=None, enable_SMTPUTF8=False,
                 #  decode_data=False, default_channel=None, username=None,
                 #  icon_url=None):
        #  super().__init__(localaddr, remoteaddr, data_size_limit, map,
                         #  enable_SMTPUTF8, decode_data)

        #  self.webhook_url = webhook_url
        #  self.default_channel = default_channel
        #  self.username = username
        #  self.icon_url = icon_url

        #  self.rules = None

    #  def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
        #  """Process incoming mail to webhook"""

        #  msg = email.message_from_bytes(data)
        #  send, channel = evaluate_message(msg, self.rules, self.default_channel)
        #  if send:
            #  text = format_mail(msg)
            #  try:
                #  send_to_mattermost(self.webhook_url, text, channel,
                                   #  self.username, self.icon_url)
                #  print('OK')
            #  except M2MBException as err:
                #  print("Something went wrong when sending message")
                #  print(err.args)

    #  def load_filter(self, sieve_file):
        #  """Loads sieve rules from file to apply to recieved mails."""

        #  with open(sieve_file, encoding="utf-8") as sfile:
            #  self.rules = sifter.parser.parse_file(sfile)
