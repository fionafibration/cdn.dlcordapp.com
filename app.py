#!/usr/bin/env python3

from flask import Flask, escape, request, redirect

app = Flask(__name__)


# Crappy way to detect if we're getting indexed by the Discord web crawler for embedding
def is_embed():
    ua_string = request.user_agent.string

    return ("DiscordBot" in ua_string or \
            "+https://discordapp.com" in ua_string \
    )



@app.route('/')
def hello():
    agent = request.headers.get('User-Agent')
    return f'User Agent String: {escape(agent)}'



@app.route('/attachments/<path:cdn_content>')
def discord_image(cdn_content):

    # We're being embedded, send normal content
    if is_embed():
        return redirect(f"https://cdn.discordapp.com/attachments/{cdn_content}")

    # User opened in browser
    else:
        # NEVER GONNA GIVE YOU UP! NEVER GONNA LET YOU DOWN!!
        return redirect(f"https://www.youtube.com/watch?v=dQw4w9WgXcQ")

