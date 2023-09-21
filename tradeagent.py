"""
TradeAgent class
Interface to trade agent using langchain and OpenAI/AutoGPT
Will try other bases than OpenAI 
"""
import os
import uuid
import logging
import sys
from datetime import datetime

from langchain.agents import Tool
# from langchain.utilities import BashProcess
from langchain.tools.file_management.write import WriteFileTool
from langchain.tools.file_management.read import ReadFileTool
# from langchain.tools.python.tool import PythonREPLTool
# from langchain.utilities import GoogleSearchAPIWrapper
from langchain.utilities import BingSearchAPIWrapper
from langchain.tools import DuckDuckGoSearchRun
from langchain.vectorstores.redis import Redis
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
# from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.experimental import AutoGPT
from langchain.memory.chat_message_histories import FileChatMessageHistory
from langchain.utilities.wolfram_alpha import WolframAlphaAPIWrapper

from tools.stream_to_logger import StreamToLogger

class TradeAgent:
    def __init__(self, goals=None):
        self.uuid = str(uuid.uuid4()).replace('-', '')

        # setup logging
        self.logs_path = os.path.abspath("logs/")
        self.logging_file_name = f"log{datetime.now().strftime('%Y%m%d_%H%M')}_{self.uuid}.txt"
        self.logging_file_path =  f"{self.logs_path}/{self.logging_file_name}"
        self.chat_history = f"{self.logs_path}/ch{datetime.now().strftime('%Y%m%d_%H%M')}_{self.uuid}.txt"

        if not os.path.exists(self.logs_path):
            os.makedirs(self.logs_path)

        if not os.path.exists(self.logging_file_path):
            open(self.logging_file_path, "w").close()

        logging.basicConfig(
            filename=self.logging_file_path,
            level=logging.INFO,
            format="\n%(message)s\n")
        self.logging = logging.getLogger(__name__)
        sys.stdout = StreamToLogger(self.logging, logging.INFO)

        # setup embeddings and vector store
        self.embeddings = OpenAIEmbeddings()
        try:
            Redis.from_texts(
                texts=["hacker"],
                redis_url=os.environ["REDIS_URL"],
                index_name=self.uuid,
                embedding=self.embeddings
            )

            self.vectorstore = Redis(
                redis_url=os.environ["REDIS_URL"],
                index_name=self.uuid,
                embedding_function=self.embeddings.embed_query
            )
        except Exception as err:
            print("Redis vectorstore creation failed: {err}")
            # print("FAISS creation failed {err}")
            # yield err
            raise err
        
        # set the goals
        if goals:
            self.goals = goals
        else:
            self.goals = [
                "Conduct extensive research and anlysis of US NASDAQ stock market data focusing NASDAQ 100 technology sector index companies",
                "Create an extensive trading strategy using traditional trading techniques that will minimize risk and maximize profit",
                # "Do backtesting of your strategies with the python library backtrader using the documentation at https://github.com/mementum/backtrader"
                "Continuously monitor the stock market conditions to ensure consistent proformance and adapt to a changing market",
                # "Provide performance reports and analysis to make data driven decisions to improve your returns",
                "Insure strict adherence to all ethical and legal standards in all tradining activities to ensure compliance with regulatory requirements and protection of investments",
                "Create a list of stocks to buy with suggestions to create an intraday profit in a text file called suggestions.txt",
                "Finish after suggestions.txt is created"
            ]
        
        # set the autogpt agent and tools
        self.llm = ChatOpenAI(temperature=0)

        # set the langtool tools
        self.tools = [
            # Tool(
            #     "search",
            #     GoogleSearchAPIWrapper().run,
            #     """
            #     Useful for when you need to answer questions about current events. 
            #     You should ask targeted questions
            #     """
            # ),
            Tool(
                "search",
                BingSearchAPIWrapper().run,
                """
                Searching the internet
                """
            ),
            Tool(
                "search_2",
                DuckDuckGoSearchRun().run,
                """
                Another tool for searching the internet
                """
            ),

            # PythonREPLTool(),
            # # ShellTool(),
            # Tool(
            #     "bash",
            #     BashProcess().run,
            #     "useful for when you want to run a command in the bash terminal."
            # ),
            Tool(
                "wolfram_alpha",
                WolframAlphaAPIWrapper().run,
                """
                Using wolfram alpha for computation and presentation
                """
            ),

            WriteFileTool(),
            ReadFileTool()
        ]

        self.agent = AutoGPT.from_llm_and_tools(
            ai_name="Gordon Gekko",
            ai_role="Expert Stock Trader",
            tools=self.tools,
            llm=self.llm,
            memory=self.vectorstore.as_retriever(),
            chat_history_memory=FileChatMessageHistory(self.chat_history)
        )
        self.agent.chain.verbose = False
        # self.agent = initialize_agent(
        #     self.tools, 
        #     self.llm, 
        #     agent=AgentType.OPENAI_FUNCTIONS, 
        #     verbose=True
        # )
        self.autogpt_resp = ""
    
    def run(self):
        try:
            self.autogpt_resp = self.agent.run(self.goals)
        except Exception as err:
            print(f"AutoGPT failure {err}")

        if self.autogpt_resp:
            self.logging.info(f"AutoGPT Response: {self.autogpt_resp}")



