from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.summarize import load_summarize_chain

from config import Config


class Summarizer:
    def __init__(self):
        self.model = ChatGoogleGenerativeAI(
            model=Config.gemini_model, google_api_key=Config.gemini_api_key)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000, chunk_overlap=200)
        self.chain = load_summarize_chain(self.model, chain_type="map_reduce")

    def summarize(self, text: str) -> str:
        docs = self.text_splitter.create_documents([text])
        return self.chain.invoke(docs)['output_text']
