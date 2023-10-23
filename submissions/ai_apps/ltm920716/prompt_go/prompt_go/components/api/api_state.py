import reflex as rx
from prompt_go.states import State
from typing import List, Dict, Union


class ApiState(State):

    api_list: List[Dict[str, Union[str, list]]] = [
        {
            "api_name": "chatgpt",
            "api_version": "0.1.0",
            "api_url": "https://api.openai.com/v1/completions",
            "params": ["model", "temperatue"],
            "tips": "Built in ChatAPI",
            "type": "chat"
        },
        {
            "api_name": "Manually",
            "api_version": "0.1.1",
            "api_url": "",
            "params": [],
            "tips": "Built in manual scoring API",
            "type": "score"
        },
        {
            "api_name": "AI-Score",
            "api_version": "0.0.1",
            "api_url": "",
            "params": [],
            "tips": "Built in automatic scoring API",
            "type": "score"
        }
    ]

    api_types: List[str] = [
        "chat",
        "score",
        "normal"
    ]
