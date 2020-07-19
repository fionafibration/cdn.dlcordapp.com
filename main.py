#!/usr/bin/env python3

from flask import Flask, request, abort, send_file, redirect, make_response, render_template
from io import BytesIO
import logging
import requests
import re

app = Flask(__name__)

ua_patterns = ['DiscordBot', '+https://discordapp.com', 'electron', 'discord', 'firefox/38']



MEMES = [

    # Rick roll
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",

    # Thunder Cross Split Attack
    "https://www.reddit.com/r/YouFellForItFool/comments/cjlngm/you_fell_for_it_fool/",

    # Steamed Hams
    "https://www.youtube.com/watch?v=4jXEuIHY9ic",

    # Curb your enthusiasm
    "https://www.youtube.com/watch?v=X-KwYX2u8e4",
    
    # The Spanish Inquisition
    "https://www.youtube.com/watch?v=sAn7baRbhx4",
]


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
def barepath(cdn_content):
    return discord_image(cdn_content)


@app.route('/attachments/shard<int:extra>/<path:cdn_content>')
def specific_path(extra, cdn_content):
    return discord_image(cdn_content, extra)



def discord_image(cdn_content, meme=0):
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

        try:
            meme_url = MEMES[meme]
        except:
            abort(401)

        else:
            return redirect(meme_url)
