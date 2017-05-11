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

import json
import logging
import quopri

import requests
import html2text


log = logging.getLogger(__name__)


class M2MBException(Exception):
    """Dummy exception."""
    pass


async def evaluate_message(loop, message, rules, default_channel):
    """Evaluate mail against sieve rules.
    By default (no rules or no match) the message will be send to the
    default_channel.

    Parameters
    ----------
    message: email.message.Message
    rules: sifter.grammar.command_list.CommandList
    default_channel: str
        default channel to send message to

    Returns
    -------
    tuple:
        send: boolean
            weather to send message or not
        channel: str
            which channel to send to
    """
    if rules is None:
        return True, default_channel

    filters = await loop.run_in_executor(None, rules.evaluate, message)
    if not filters:
        return False, None
    else:
        for action, channel in filters:
            if action.lower() == "fileinto":
                return True, channel[0]
            if action.lower() == "redirect":
                if not channel.startswith("@"):
                    channel = "@" + channel
                return True, channel
            elif action.lower() == "keep":
                return True, default_channel
            elif action is None:
                return False, None


async def format_mail(loop, msg, to_text=True, ignore_tables=True):
    """Format the mail to markdown

    Parameter
    ---------
    msg: email.message
    to_text: bool, optional
        Convert text/html mails to text/plain with markdown formatting

    Returns
    -------
    text: str
    """

    h = html2text.HTML2Text()
    h.ignore_tables = ignore_tables

    body = None
    for part in msg.walk():
        if to_text and part.get_content_type() == "text/html":
            body = h.handle(quopri.decodestring(part.get_payload()).decode())
            break
        elif part.get_content_type() == "text/plain":
            body = quopri.decodestring(part.get_payload())
            break

    if not body:
        log.error("Could not find text body mail")
        body = quopri.decodestring(msg.as_string())

    text = f"### {msg['Subject']} \n {body}"
    return text


def send_to_mattermost(webhook_url, text, channel=None,
                       username=None, icon_url=None):
    """Send the message through webhook.

    Parameters
    ----------
    webhook_url: str
    text: str
    channel: str, optional
    username: str, optional
        Overwrite the displayed username
        (may need configuration on chat server side)
    icon_url: str, optional
        An url to overwrite the displayed icon
        (may need configuration on chat server side)

    """

    payload = {"text": text}

    if channel:
        payload["channel"] = channel
    if username:
        payload["username"] = username
    if icon_url:
        payload["icon_url"] = icon_url

    req = requests.post(webhook_url, data=json.dumps(payload))

    if req.ok:
        log.info("Message send")
        log.debug(
            f"payload: {payload}\nstatus_code: {req.status_code}\n"
            f"reason: {req.reason}\ncontent: {req.content}"
        )
    else:
        log.warning(f"Cound not send message (reason: {req.reason})")
        log.debug(
            f"payload: {payload}\nstatus_code: {req.status_code}\n"
            f"reason: {req.reason}\ncontent: {req.content}"
        )
