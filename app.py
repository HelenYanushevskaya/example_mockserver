import os

import requests
from flask import Flask, render_template

app = Flask(__name__)

os.environ['HTTP_PROXY'] = 'http://0.0.0.0:1080'

json_messages = {
    'result': [
        {
            "text": "Hello!",
            "date_created": "2021-09-17T18:34:35"
        },
        {
            "id": 1608090,
            "text": "Hello world!",
            "date_created": "2021-07-29T11:24:53"
        },
        {
            "id": 569391,
            "text": "welcome to the messages",
            "date_created": "2021-05-12T18:00:45"
        }
    ]
}

@app.route('/messages')
def messages():
    return json_messages


@app.route('/messages_auth')
def messages_auth():
    response = requests.get("http://192.168.1.233:1082/authorization")
    if response.status_code == 200:
        return json_messages
    else:
        return {"error": "Authorization failed"}

@app.route('/auth')
def auth():
    response = requests.get("http://192.168.1.233:1082/authorization")
    if response.status_code == 200:
        message = 'Authorization success'
    else:
        message = 'Authorization failed'
    return render_template("index.html", message=message)


@app.route('/')
def base():
    message = 'Check browser'
    return render_template("index.html", message=message)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=1081)
