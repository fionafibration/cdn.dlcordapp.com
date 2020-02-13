from flask import Flask, escape, request

app = Flask(__name__)

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    agent = request.headers.get('User-Agent')
    return f'Hello, {escape(name)}! {escape()}'
