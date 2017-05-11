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
            text = await format_mail(server.loop, message, server.to_text,
                                     server.ignore_tables)
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
                 sieve_file=None,
                 to_text=True,
                 ignore_tables=True):
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
        self.to_text = to_text
        self.ignore_tables = ignore_tables

        if sieve_file:
            with open(sieve_file, newline="\r\n") as sfile:
                self.rules = sifter.parser.parse_file(sfile)
