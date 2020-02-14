#!/usr/bin/env python3

from flask import Flask, request, abort, send_file, redirect, make_response, escape
from io import BytesIO
import logging
import requests

app = Flask(__name__)

ua_patterns = ['DiscordBot', '+https://discordapp.com', 'electron', 'discord', 'firefox/38']

# Crappy way to detect if we're getting indexed by the Discord web crawler for embedding
def is_embed():
    ua_string = request.user_agent.string.lower()

    logging.warn(ua_string)

    for pattern in ua_patterns:
        if pattern.lower() in ua_string:
            return True

    return False


@app.route('/')
def hello():
    agent = request.headers.get('User-Agent')
    return f'User Agent String: {escape(agent)}'



@app.route('/attachments/<path:cdn_content>')
def discord_image(cdn_content):

    # We're being embedded, send normal content
    if is_embed():
        dresp = requests.get(f"https://cdn.discordapp.com/attachments/{cdn_content}")

        if dresp.status_code != 200:
            return abort(404)

        content = BytesIO(dresp.content)

        resp = make_response(send_file(content, mimetype=dresp.headers["content-type"]))

        resp.headers["connection"] = "keep-alive"

        resp.headers["vary"] = "User-Agent, Content-Encoding"

        return resp

        # resp = make_response("", 308)
        # resp.mimetype = "image/png"

        # resp.headers["Location"] = f"https://cdn.discordapp.com/attachments/{cdn_content}"

        # return resp

    # User opened in browser
    else:
        # NEVER GONNA GIVE YOU UP! NEVER GONNA LET YOU DOWN!!
        return redirect(f"https://www.youtube.com/watch?v=dQw4w9WgXcQ")
