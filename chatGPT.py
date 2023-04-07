# import the liberary
from prompt import Prompt
import os
from langchain import OpenAI
from llama_index import SimpleDirectoryReader, GPTSimpleVectorIndex
# from IPython.display import Markdown, display
from llama_index.node_parser import SimpleNodeParser

# the api of ChatGPT
os.environ["OPENAI_API_KEY"] = "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"

def construct_index(directory_path):
    documents = SimpleDirectoryReader(directory_path).load_data()
    parser = SimpleNodeParser()
    nodes = parser.get_nodes_from_documents(documents)
    index = GPTSimpleVectorIndex(nodes)
    index.save_to_disk('index.json')
    return index

class ChatGPT:
    def __init__(self):
        self.prompt = Prompt()
        self.model = os.getenv("OPENAI_MODEL", default = "text-davinci-003")               
        self.temperature = float(os.getenv("OPENAI_TEMPERATURE", default = 0))              
        self.frequency_penalty = float(os.getenv("OPENAI_FREQUENCY_PENALTY", default = 0)) 
        self.presence_penalty = float(os.getenv("OPENAI_PRESENCE_PENALTY", default = 0.6))
        self.max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", default = 240))   
        self.index = construct_index('context_data/data')
    
    def get_response(self):
        response = self.index.query(self.prompt.generate_prompt(), response_mode="default")
        return f"{response.response}"

    def add_msg(self, text):
        self.prompt.add_msg(text)