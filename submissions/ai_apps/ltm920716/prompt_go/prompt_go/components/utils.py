from __future__ import annotations
from typing import Literal

import reflex as rx
from reflex.components.libs.chakra import ChakraComponent

import openai


# https://github.com/reflex-dev/reflex/issues/358#issuecomment-1748826100

class ToastProvider(ChakraComponent):
    tag = "useToast"

    def _get_hooks(self) -> str | None:
        return "refs['__toast'] = useToast()"

    @staticmethod
    def show(
        title: str,
        description: str,
        duration: int,
        status: Literal["info", "warning",
                        "success", "error", "loading"] = "info",
    ) -> rx.event.EventSpec:
        return rx.call_script(
            f"""
            refs['__toast']({{
            title: "{title}",
            description: "{description}",
            duration: {duration},
            status: "{status}",
            isClosable: true,
            }})
        """
        )


INSTRUCTION_OUTPUT_EVAL = """You are now a chat model scoring assistant, providing you with history dialogues、assistant output and expected output of the chat model. 
You need to rate the last chat output based on the corresponding history instruction and expected output. 
The scoring range is [0,1,2,3,4,5]. 
The content between >>> and <<< bellow is the content of history、assistant output and expected output.

>>>
{input_pred_gt_dict}
<<<

Remener only return score! 
Score:
"""


INSTRUCTION_EVAL = """You are now a chat model scoring assistant, providing you with history dialogues and assistant output of the chat model. 
You need to rate the prediction based on the corresponding instruction. 
Taking into account whether the structure、style、and specific content of output is fitted to the instruction.
The scoring range is [0,1,2,3,4,5]. 
The content between >>> and <<< bellow is the content of history and assistant output.

>>>
{input_pred_dict}
<<<

Remener only return score! 
Score:
"""


def openai_chat(messages: list, model="gpt-3.5-turbo", temperature=0) -> str:
    return openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature
    ).choices[0].message.content
