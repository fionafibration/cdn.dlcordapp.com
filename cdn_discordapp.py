from flask import Flask, escape, request

app = Flask(__name__)

@app.route('/')
def hello():
    agent = request.headers.get('User-Agent')
    return f'User Agent String: {escape(agent)}'
