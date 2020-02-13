#!/usr/bin/env python3

from flask import Flask, escape, request, redirect, make_response
from io import BytesIO
import requests

app = Flask(__name__)

ua_patterns = ['DiscordBot', '+https://discordapp.com', 'electron']

# Crappy way to detect if we're getting indexed by the Discord web crawler for embedding
def is_embed():
    ua_string = request.user_agent.string

    return any([pattern in ua_string for pattern in ua_patterns])



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

        return send_file(content)

        # resp = make_response("", 308)
        # resp.mimetype = "image/png"

        # resp.headers["Location"] = f"https://cdn.discordapp.com/attachments/{cdn_content}"

        # return resp

    # User opened in browser
    else:
        # NEVER GONNA GIVE YOU UP! NEVER GONNA LET YOU DOWN!!
        return redirect(f"https://www.youtube.com/watch?v=dQw4w9WgXcQ")

