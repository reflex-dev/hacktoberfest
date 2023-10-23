import reflex as rx
import os
import openai
from datetime import datetime
from sqlalchemy.sql import func
import aiohttp

from dotenv import load_dotenv

if os.path.exists('.env'):
    load_dotenv('.env')
openai.api_key = os.getenv('OPENAI_API_KEY')
assert openai.api_key, 'Init OpenAI API Key First!'


class User(rx.Model, table=True):
    username: str
    password: str
    created_at: datetime = func.now()


class ChatNode(rx.Model, table=True):
    username: str
    node_name: str
    node_version: str
    api_model: str
    api_temperature: float
    prompts: str
    description: str = ''
    created_at: datetime = func.now()


class ChatRunRecord(rx.Model, table=True):
    chat_result: str
    node_name: str
    node_version: str
    dataset: str
    items: int
    time_stamp: str
    iteration: int
    score_api: str


class Dataset(rx.Model, table=True):
    dataset_name: str
    description: str = ''
    username: str
    source: str


async def make_async_request(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


class State(rx.State):
    """The app state."""

    username: str = 'test'
    hello_word: bool = True
    open_history: bool = False
    open_pipeline: bool = False
    open_api: bool = False
    open_dataset: bool = False

    def pipeline_show(self):
        self.open_pipeline = True
        self.open_api = False
        self.open_dataset = False
        self.open_history = False
        self.hello_word = False

    def history_show(self):
        self.open_pipeline = False
        self.open_api = False
        self.open_dataset = False
        self.open_history = True
        self.hello_word = False

    def api_show(self):
        self.open_pipeline = False
        self.open_api = True
        self.open_dataset = False
        self.open_history = False
        self.hello_word = False

    def dataset_show(self):
        self.open_pipeline = False
        self.open_api = False
        self.open_dataset = True
        self.open_history = False
        self.hello_word = False
