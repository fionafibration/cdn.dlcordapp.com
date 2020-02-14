#!/usr/bin/env python3

from flask import Flask, request, abort, send_file, redirect, make_response, render_template
from io import BytesIO
import logging
import requests
import re

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
def index():
    return render_template('index.html')


# CDN Regex

CDN_REGEX = re.compile("""([^{}|\\^\[\]`<>#;\/?:@&=+$,]{1,50}\/)([^{}|\\^\[\]`<>#;\/?:@&=+$,]{1,50}\/)([^{}|\\^\[\]`<>#;\/?:@&=+$,]{1,50})""")

@app.route('/attachments/<path:cdn_content>')
def discord_image(cdn_content):

    match = CDN_REGEX.match(cdn_content)

    # We're being embedded, send normal content
    if is_embed() and match != None:
        dresp = requests.get(f"https://cdn.discordapp.com/attachments/{cdn_content}")

        if dresp.status_code == 404:
            return abort(404)


        elif dresp.status_code != 200:
            return abort(401)

        # 10 mb stream limit
        if dresp.headers['content-length'] >= 1e7:
            return abort(403)

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
