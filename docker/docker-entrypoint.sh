#!/bin/bash

if [ -z "$WEBHOOK_URL" ]; then
    echo "You must provide the WEBHOOK_URL environment variable"
    exit 1
fi

cmd_options=""

if [ -n "$DEFAULT_CHANNEL" ]; then
    cmd_options="$cmd_options --default_channel $DEFAULT_CHANNEL"
fi

if [ -n "$USERNAME" ]; then
    cmd_options="$cmd_options --username $USERNAME"
fi

if [ -n "$ICON_URL" ]; then
    cmd_options="$cmd_options --icon_url $ICON_URL"
fi

if [ -n "$NO_HTML2TEXT" -a "$NO_HTML2TEXT" == "true" ]; then
    cmd_options="$cmd_options --no_html2text"
fi

if [ -n "$NO_IGNORE_TABLES" -a "$NO_IGNORE_TABLES" == "true" ]; then
    cmd_options="cmd_options --no_ignore_tables"
fi

if [ -e /rules.sieve ]; then
    cmd_options="$cmd_options --sieve_rules_file /rules.sieve"
fi

if [ -n "$DEBUG_LEVEL" ]; then
    for i in $(seq 1 $DEBUG_LEVEL); do
        cmd_options="$cmd_options -d"
    done
fi

m2mbd $(hostname -i) 25 $WEBHOOK_URL $cmd_options
