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
import unittest
import email
import smtplib
import logging
import pkg_resources

from urllib.parse import urlparse
from functools import partial

from aiohttp import web

from m2mb.core import M2MBServer
from m2mb.tests.utils import handle_incoming_webhook, asend_mail


class TestM2MBServer(unittest.TestCase):

    GOOD_WEBHOOK_URL = "http://localhost:8283/hooks/abcdefghijklmnopqrstuvwxyz0"
    BAD_WEBHOOK_URL = "http://localhost:8283/hooks/badwebhook"
    DEFAULT_CHANNEL = "general"
    USERNAME = "M2MB"

    def setUp(self):
        self._old_loop = asyncio.get_event_loop()
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        #  logging.basicConfig(level=logging.DEBUG)
        #  self.loop.set_debug(True)

        self.parsed_url = urlparse(self.GOOD_WEBHOOK_URL)
        dummy_mattermost_api_app = web.Application()
        dummy_mattermost_api_app.router.add_post(
            "/hooks/{webhook_id}",
            partial(handle_incoming_webhook,
                    webhook_urls=[self.parsed_url.path])
        )
        dummy_mattermost_api_factory = self.loop.create_server(
            dummy_mattermost_api_app.make_handler(),
            *self.parsed_url.netloc.split(":")
        )
        self.dummy_mattermost_api_server = self.loop.run_until_complete(dummy_mattermost_api_factory)

    def m2mb_factory(self, webhook_url, sieve_file=None):
        def factory():
            return M2MBServer(webhook_url,
                              hostname="unittests M2MBServer",
                              #  default_channel="general",
                              #  username="M2MB",
                              default_channel=self.DEFAULT_CHANNEL,
                              username=self.USERNAME,
                              loop=self.loop,
                              sieve_file=sieve_file)
        return factory

    def tearDown(self):
        self.dummy_mattermost_api_server.close()
        self.loop.run_until_complete(self.dummy_mattermost_api_server.wait_closed())
        self.loop.close()
        asyncio.set_event_loop(self._old_loop)

    def test_no_sieve_rules(self):
        m2mbserver = self.loop.run_until_complete(
            self.loop.create_server(self.m2mb_factory(self.GOOD_WEBHOOK_URL),
            "localhost",
            8225)
        )

        async def end_test(loop):
            await asend_mail(loop,
                             "localhost",
                             8225,
                             "sender@example.org",
                             "receiver@example.org",
                             "body test")
            loop.stop()

        asyncio.ensure_future(end_test(self.loop))
        self.loop.run_forever()
        m2mbserver.close()
        self.loop.run_until_complete(m2mbserver.wait_closed())

    def test_sieve_rules(self):
        #  sieve_rules_file = pkg_resources.resource_filename("m2mb.tests.sieve",
                                                           #  "rules1.sieve")
        #  message = pkg_resources.resource_filename("m2mb.tests.mails",
                                                  #  "mail1.msg")
        sieve_rules_file = "./m2mb/tests/sieve/rules1.sieve"
        with open("./m2mb/tests/mails/mail1.msg") as msg1_fh, \
             open("./m2mb/tests/mails/mail2.msg") as msg2_fh, \
             open("./m2mb/tests/mails/mail3.msg") as msg3_fh, \
             open("./m2mb/tests/mails/mail4.msg") as msg4_fh:
            messages = [
                email.message_from_file(msg1_fh).as_string(),
                email.message_from_file(msg2_fh).as_string(),
                email.message_from_file(msg3_fh).as_string(),
                email.message_from_file(msg4_fh).as_string(),
            ]
        m2mbserver = self.loop.run_until_complete(
            self.loop.create_server(self.m2mb_factory(
                self.GOOD_WEBHOOK_URL,
                sieve_rules_file
            ),
            "localhost",
            8225)
        )

        async def end_test(loop):
            for message in messages:
                await asend_mail(loop,
                                 "localhost",
                                 8225,
                                 "sender@example.org",
                                 "receiver@example.org",
                                 message)
            loop.stop()

        asyncio.ensure_future(end_test(self.loop))
        self.loop.run_forever()
        m2mbserver.close()
        self.loop.run_until_complete(m2mbserver.wait_closed())
