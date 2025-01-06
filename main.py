from fastapi import FastAPI, HTTPException
from copy import deepcopy


app = FastAPI()
messages = []


class Message:
    def __init__(self, id_, content):
        self.id_ = id_
        self.content = content

    def to_dict(self):
        return {"id": self.id_, "content": self.content}


def find_message_by_id(id_):
    id_ = int(id_)
    for i, m in enumerate(messages):
        if m.id_ == id_:
            return i, m
    return -1, None


@app.post("/message")
def add_message(content):
    id_ = 0 if not messages else messages[-1].id_ + 1
    message = Message(id_, content)
    messages.append(message)
    return message.to_dict()


@app.get("/message")
def get_message(id_):
    _, message = find_message_by_id(id_)
    if not message:
        raise HTTPException(status_code=404)
    return message.to_dict()


@app.get("/messages")
def get_messages():
    return {"messages": [message.to_dict() for message in messages]}


@app.delete("/message")
def delete_message(id_):
    i, message = find_message_by_id(id_)
    if not message:
        raise HTTPException(status_code=404)
    message_dc = deepcopy(message)
    del messages[i]
    return message_dc.to_dict()
