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
import json
import logging
import random
import smtplib

from functools import partial

from aiohttp import web


async def handle_incoming_webhook(request, webhook_urls):
    request_id = "".join(random.choice("0123456789abcdef") for _ in range(26))
    if request.path not in webhook_urls:
        status = 400
        body = {
            "request_id": request_id,
            "id": "web.incoming_webhook.invalid.app_error",
            "message": "Invalid webhook",
            "detailed_error": "",
            "status_code": status,
        }
        body = json.dumps(body)
        content_type = "application/json"
    else:
        data = await request.text()
        if data.startswith("payload="):
            data = data[8:]
        data = json.loads(data)
        if "channel" not in data.keys():
            data["channel"] = ""
        if data["channel"].startswith("@non-existing"):
            status = 400
            body = {
                "request_id": request_id,
                "id": "web.incoming_webhook.user.app_error",
                "message": "Couldn't find the user",
                "detailed_error": "",
                "status_code": status,
            }
            body = json.dumps(body)
            content_type = "application/json"
        elif data["channel"].startswith("non-existing"):
            status = 500
            body = {
                "request_id": request_id,
                "id": "web.incoming_webhook.channel.app_error",
                "message": "Couldn't find the channel",
                "detailed_error": "",
                "status_code": status,
            }
            body = json.dumps(body)
            content_type = "application/json"
        else:
            status = 200
            body = "ok"
            content_type = "text/plain"

    headers = {
        "X-Version-Id": "3.7.0.3.7.3.1ea10855d03fb507b17508bb6d2796bd.false",
        "X-Request-Id": request_id
    }
    logging.debug(f"status: {status}, text: {body}, header: {headers}")
    return web.Response(status=status, text=body, headers=headers)


async def asend_mail(loop, host, port, sender, receiver, message):
    await loop.run_in_executor(None, send_mail, host, port,
                               sender, receiver, message)


def send_mail(host, port, sender, receiver, message):
    with smtplib.SMTP(host, port) as client:
        client.ehlo(host)
        client.login("nologin", "nopasswd")
        client.sendmail(sender, receiver, message)


if __name__ == "__main__":
    app = web.Application()
    app.router.add_post("/hooks/{webhook_id}",
                        partial(handle_incoming_webhook,
                                webhook_urls=["/hooks/abc"]))

    loop = asyncio.get_event_loop()
    factory = loop.create_server(app.make_handler(), "localhost", "8283")
    server = loop.run_until_complete(factory)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()
