import reflex as rx

from langchain.chat_models import ChatOpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document


class State(rx.State):

    # The current large text to be summarized.
    large_text: str

    # openai key
    openai_api_key: str

    # the result
    summary: str

    is_loading: bool = False

    loading_text: str = ""



    def start_process(self):
        """Set state variables and summarize method."""
        self.is_loading = True
        self.loading_text = "generating summary...."

        return State.summarize



    def summarize(self):

        llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k", streaming=True, openai_api_key=self.openai_api_key)

        docs = [Document(page_content=t) for t in self.large_text]

        # use load_summarize_chain to summarize the full text and return self.summary to frontend
        chain = load_summarize_chain(llm, chain_type="stuff")

        self.summary = chain.run(docs)
        self.summary
        yield

        # reset state variable again
        self.is_loading = False
        self.loading_text = ""