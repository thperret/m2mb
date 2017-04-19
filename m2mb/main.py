# -*- coding: utf-8 -*-
"""
m2mb  Copyright (C) 2017  Thomas Perret <thomas.perret@phyx.fr>
This program comes with ABSOLUTELY NO WARRANTY; for details see COPYING.
This is free software, and you are welcome to redistribute it
under certain conditions; see LICENSE for details.
"""

import asyncio
import sys
import signal
import argparse
import logging

from m2mb.core import M2MBServer


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("host", type=str, help="Local address to bind to")
    parser.add_argument("port", type=int, help="Local port to bind to")
    parser.add_argument("webhook_url", type=str, help="Slack compatible webhook url")
    parser.add_argument("--default_channel", type=str,
                        help=("Default channel to send messages to "
                              "(defaults to webhook configuration)"),
                        default=None)
    parser.add_argument("--username", type=str, help="Displayed username",
                        default=None)
    parser.add_argument("--icon_url", type=str, help="Url for displayed icon",
                        default=None)
    parser.add_argument("--sieve_rules_file", type=str,
                        help="Sieve rules definitions file", default=None)
    parser.add_argument('-d', '--debug', default=0, action='count',
                        help="""Increase debugging output.""")
    parser.add_argument('--hostname', default=None)

    return parser.parse_args()


def main():
    args = parse_args()
    logging.basicConfig(level=logging.WARNING)
    log = logging.getLogger("m2mb")

    loop = asyncio.get_event_loop()

    if args.debug > 0:
        log.setLevel(logging.INFO)
    if args.debug > 1:
        log.setLevel(logging.DEBUG)
    if args.debug > 2:
        loop.set_debug(enabled=True)


    log.info('Server listening on %s:%s', args.host, args.port)
    m2mb_server = loop.run_until_complete(loop.create_server(
        lambda: M2MBServer(args.webhook_url,
                           hostname=args.hostname,
                           default_channel=args.default_channel,
                           username=args.username,
                           icon_url=args.icon_url,
                           loop=loop,
                           sieve_file = args.sieve_rules_file),
        args.host, args.port))
    loop.add_signal_handler(signal.SIGINT, loop.stop)
    #  if args.sieve_rules_file:
        #  m2mb_server.load_filter(args.sieve_rules_file)

    log.info('Starting asyncio loop')

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        m2mb_server.close()
        loop.run_until_complete(m2mb_server.wait_closed())
        loop.close()
        log.info('Completed asyncio loop')


if __name__ == "__main__":
    args = parse_args()
    main(args)
