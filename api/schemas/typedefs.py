import asyncio
import pinecone as pc
from aiofauna import *
from typing import *
from langchain.chains import LLMChain, create_tagging_chain_pydantic
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.prompts import ChatPromptTemplate
from langchain.schema import *
from os import environ
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor
from ..utils import run_in_threadpool, is_async_callable, ParamSpec

load_dotenv()

ai = ChatOpenAI(temperature=0.2, model="gpt-3.5-turbo-16k-0613", max_tokens=1024)  # type: ignore

T = TypeVar("T", bound="Chainable")
P = ParamSpec("P")

class Chainable(FaunaModel):
    """Schema that can be chained with other schemas"""

    _ask_for: List[str] = []
    _answers: List[str] = []

    @classmethod
    def __init_subclass__(cls: Type[T], **kwargs):
        super().__init_subclass__(**kwargs)
        for field in cls.__fields__.values():
            field.required = False
        cls.chain = create_tagging_chain_pydantic(cls, ai)

    @classmethod
    def run(cls: Type[T], text: str) -> T:
        return cls.chain.run(text)  # type: ignore

    @classmethod
    def check_what_is_empty(cls: Type[T], text: str):
        instance = cls.run(text)
        for field in cls.__fields__.keys():
            if getattr(instance, field) is None:
                cls._ask_for.append(field)
        return cls._ask_for

    @classmethod
    def prompt(cls: Type[T], ask_for: List[str]) -> str:
        first_prompt = ChatPromptTemplate.from_template(
            """
            System Message:
            I must ask the user for the following information:
            {ask_for}
             Also my customer speaks Spanish, so I will ask and answer in Spanish primarily.
            AI Message:  
            """
        )
        info_gathering_chain = LLMChain(llm=ai, prompt=first_prompt)
        ai_chat = info_gathering_chain.run(ask_for=ask_for)
        return ai_chat

    @classmethod
    async def run_until_complete(cls: Type[T], websocket: WebSocketResponse) -> T:
        """
        Communicates with the user via websocket to complete the
        Schema.
        """
        instance = cls()
        fields = instance.__fields__.keys()
        cls._ask_for = [
            field
            for field in fields
            if field not in ["ref", "ts"] and getattr(instance, field) is None
        ]
        while cls._ask_for:
            prompt = cls.prompt(cls._ask_for)
            await websocket.send_str(prompt)
            answer = await websocket.receive_str()
            cls._answers.append(answer)
            instance = cls.run("\n".join(cls._answers))
            cls._ask_for = [
                field
                for field in fields
                if field not in ["ref", "ts"] and getattr(instance, field) is None
            ]
        await websocket.send_str(
            "Thanks so much for your time, Don't hesitate to contact me if you have any questions."
        )
        return instance

class BackgroundTask:
    def __init__(
        self, func: Callable[P, Any], *args: P.args, **kwargs: P.kwargs
    ) -> None:
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.is_async = is_async_callable(func)

    async def __call__(self) -> None:
        if self.is_async:
            await self.func(*self.args, **self.kwargs)
        else:
            await run_in_threadpool(self.func, *self.args, **self.kwargs)


class BackgroundTasks(BackgroundTask):
    def __init__(self, tasks: Optional[Sequence[BackgroundTask]] = None):
        self.tasks = list(tasks) if tasks else []

    def add_task(
        self, func: Callable[P, Any], *args: P.args, **kwargs: P.kwargs
    ) -> None:
        task = BackgroundTask(func, *args, **kwargs)
        self.tasks.append(task)

    async def __call__(self) -> None:
        for task in self.tasks:
            await task()
        
        
 
class ChatBotModel(BaseModel):
    """A chatbot model"""
    chatbot_name:str=Field(default="Bot")
    role:str=Field(default="assistant")
    action:str=Field(default="answer any question")
    topic:str=Field(default="what user is asking")
    goal:str=Field(default="help the user to have an amazing experience")
    personality:str=Field(default="helpful, truthful, creative")
    attitude:str=Field(default="polite")
    
class DocumentModel(BaseModel):
    namespace:str=Field(default="default")
    text:str=Field(...)