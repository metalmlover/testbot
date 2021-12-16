from flask import Flask, request, Response
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings, ConversationState, MemoryStorage
from botbuilder.schema import Activity
import asyncio
from qnabot import QnaBot

application = Flask(__name__)
loop = asyncio.get_event_loop()

botsettings = BotFrameworkAdapterSettings(
    "1e73c813-4336-4621-ac2f-921109e76492", "RGK7Q~jaqNYBH7A~oZzRVl8fu2v54C1Ye8d-.")
botadapter = BotFrameworkAdapter(botsettings)

CONMEMORY = ConversationState(MemoryStorage())
botdialog = QnaBot()


@application.route("/")
def hello():
    return {"result": "You successfully created your first route!"}


@application.route("/api/messages", methods=["POST"])
def messages():
    if "application/json" in request.headers["content-type"]:
        body = request.json
    else:
        return Response(status=415)

    activity = Activity().deserialize(body)

    auth_header = (request.headers["Authorization"]
                   if "Authorization" in request.headers else "")

    async def call_fun(turncontext):
        await botdialog.on_turn(turncontext)

    task = loop.create_task(
        botadapter.process_activity(activity, auth_header, call_fun)
    )
    loop.run_until_complete(task)

    return '200'


if __name__ == '__main__':
    application.run('localhost', 5000)
