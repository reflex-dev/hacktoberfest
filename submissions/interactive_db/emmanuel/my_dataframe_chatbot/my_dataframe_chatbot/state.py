# import reflex
import reflex as rx

from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType

import pandas as pd

import os


class State(rx.State):

    # The current question being asked.
    question: str

    error_texts: str

    # Keep track of the chat history as a list of (question, answer) tuples.
    chat_history: list[tuple[str, str]]

    openai_api_key: str

    # The files to show.
    csv_file: list[str]

    upload_confirmation: str = ""

    file_path: str

    is_loaded_skeleton: bool = True


    async def handle_upload(
        self, files: list[rx.UploadFile]
    ):
        """Handle the upload of file(s).

        Args:
            files: The uploaded files.
        """
        for file in files:
            upload_data = await file.read()
            outfile = rx.get_asset_path(file.filename)
            self.file_path = outfile

            # Save the file.
            with open(outfile, "wb") as file_object:
                file_object.write(upload_data)

            # Update the csv_file var.
            self.csv_file.append(file.filename)

            self.upload_confirmation = "csv file uploaded successfully, you can now interact with your data"



    def answer(self):
        # turn loading state of the skeleton component to False
        self.is_loaded_skeleton = False
        yield


        # check if openai_api_key is empty to return an error
        if self.openai_api_key == "":
            self.error_texts = "enter your openai api"
            return

        # check if csv_file is empty to return an error
        if not self.csv_file:
            self.error_texts = "ensure you upload a csv file and enter your openai api key"
            return


        if os.path.exists(self.file_path):
            df = pd.read_csv(self.file_path)
        else:
            self.error_texts = "ensure you upload a csv file"
            return

        # initializes an agent for working with a chatbot and integrates it with a Pandas DataFrame
        agent = create_pandas_dataframe_agent(
                    ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613", openai_api_key=self.openai_api_key),
                    df,
                    verbose=True,
                    agent_type=AgentType.OPENAI_FUNCTIONS,
                )


        self.upload_confirmation = ""

        # Add to the answer as the chatbot responds.
        answer = ""
        self.chat_history.append((self.question, answer))
        yield

        # run the agent against a question
        output = agent.run(self.question)

        self.is_loaded_skeleton = True

        # Clear the question input.
        self.question = ""

        # Yield here to clear the frontend input before continuing.
        yield

        # update answer from output
        for item in output:
            answer += item
            self.chat_history[-1] = (
                self.chat_history[-1][0],
                answer,
            )
            yield