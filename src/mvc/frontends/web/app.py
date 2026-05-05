import chainlit as cl
from langchain_core.runnables import Runnable, RunnableConfig
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser

from mvc.config import OPENROUTER_API_KEY, MODEL_NAME
from mvc.model import Workflow
from mvc.services.llm import new_llm


@cl.on_chat_start
async def on_chat_start():
    llm = new_llm(
        model=MODEL_NAME,
        openrouter_api_key=OPENROUTER_API_KEY,
        streaming=True,
    )
    workflow = Workflow(llm=llm)
    cl.user_session.set("workflow", workflow)

@cl.on_message
async def on_message(message: cl.Message):
    workflow: Workflow = cl.user_session.get("workflow")
    msg = cl.Message(content="")
    async for chunk in workflow.astream(message.content):
        await msg.stream_token(chunk)
    await msg.send()
