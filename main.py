from fastapi import FastAPI, HTTPException
from copy import deepcopy


app = FastAPI()
messages = {}


class Message:
    def __init__(self, key, content):
        self.key = key
        self.content = content

    def to_dict(self):
        return {"key": self.key, "content": self.content}


@app.post("/message")
def add_message(key, content):
    message = Message(key, content)
    messages[key] = message
    return message.to_dict()


@app.get("/message")
def get_message(key):
    if key not in messages:
        raise HTTPException(status_code=404)
    message = messages[key]
    return message.to_dict()


@app.get("/messages")
def get_messages():
    return {"messages": [message.to_dict() for message in messages.values()]}


@app.delete("/message")
def delete_message(key):
    if key not in messages:
        raise HTTPException(status_code=404)
    message = messages[key]
    message_dc = deepcopy(message)
    del messages[key]
    return message_dc.to_dict()
