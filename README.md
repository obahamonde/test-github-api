Please write an async function that takes an url as input and ingest into pinecone database all the webpages conteneet without the markdown within that url using the sitemap.xml document or traditional web crawling. It must use aiohttp ClientSession object and must have as input the configuration from aiohttp Cliensession with sensible defaults as a pydantic BaseModel, also will use bs4 and lxml for the markdown parsing and must save the page content as metadata to pinecone and use embedding from openai API ada endpoint, here is the code for the embeddings and the pinecone client:

```python

from importlib import metadata
from uuid import uuid4

from aiofauna import *
from numpy import isin
from pydantic import Field

from ..config import env
from ..schemas.typedefs import *


class Embedding(BaseModel):
    values:Vector = Field(..., title="The vector to use")
    metadata:MetaData = Field(..., title="The metadata to use")
    id:str = Field(default_factory=lambda: str(uuid4()))


class Usage(BaseModel):
    prompt_tokens: int = Field(default=0)
    total_tokens: int = Field(default=0)
    completion_tokens:Optional[int] = Field(default=None)


class EmbeddingUpsert(BaseModel):
    vectors:List[Embedding] = Field(...)
    namespace:str = Field(default="default")
    
    
class EmbeddingQuery(BaseModel):
    namespace:str
    top_k:int = Field(default=4)
    vector:Vector = Field(...)
    
    
class EmbeddingInput(BaseModel):
    model:str = Field(default="text-embedding-ada-002")
    input:str = Field(...)
    
class EmbeddingsMatch(Embedding):
    score:float = Field(...)
  
class EmbeddingCreateObject(BaseModel):
    object:str = Field(default="embedding")
    embedding:Vector = Field(...)
    index: int = Field(...)
    
    
class EmbeddingCreateResponse(BaseModel):
    object:str = Field(default="list")
    model:str = Field(default="text-embedding-ada-002")
    data:List[EmbeddingCreateObject] = Field(...)
    usage:Usage = Field(...)
    
class EmbeddingQueryResponse(BaseModel):
    namespace:str = Field(...)
    matches:List[EmbeddingsMatch] = Field(...)
    
    
class OpenAIVectors(ApiClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = "https://api.openai.com/v1/"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {env.OPENAI_API_KEY}"
        }
        
    async def create_embeddings(self, text:str):  
        response = await self.fetch(
            "embeddings",
            method="POST",
            json=EmbeddingInput(input=text).dict()
        )
        assert isinstance(response, dict)
        return EmbeddingCreateResponse(**response)
    

class PineConeClient(ApiClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = "https://aiofauna-8360578.svc.us-central1-gcp.pinecone.io"
        self.headers = {
            "Content-Type": "application/json",
            "api-key": env.PINECONE_API_KEY
        }   
        
    async def upsert(self, vectors:EmbeddingUpsert):
        response = await self.fetch(
            "/vectors/upsert",
            method="POST",
            headers=self.headers,
            json=vectors.dict()
        )
        assert isinstance(response, dict)
        
    
    async def query(self, query:EmbeddingQuery):
        response = await self.fetch(
            "/query",
            "POST",
            headers=self.headers,
            json=query.dict()
        )
        if isinstance(response, dict):
            return EmbeddingQueryResponse(**response)
        return EmbeddingQueryResponse(namespace=query.namespace, matches=[])



from __future__ import annotations
from ..schemas.typedefs import *
from aiofauna import *
from .pinecone import *
from openai_function_call import openai_function, openai_schema

Role = Literal["user", "assistant", "system", "function"]

class Message(BaseModel):
    role:Role = Field(..., description="The role of the message")
    content:str = Field(..., description="The content of the message")
    
class Choice(BaseModel):
    message:Message = Field(..., description="The message of the choice" )
    index:int = Field(..., description="The index of the choice")
    finish_reason:Optional[str] = Field(None, description="The finish reason of the choice")
    
class ChatCompletionResponse(BaseModel):
    id:str = Field(..., description="The id of the completion")
    object:str = Field(..., description="The object of the completion")
    created:int = Field(..., description="The created timestamp of the completion")
    choices:List[Choice] = Field(..., description="The choices of the completion")
    usage:Usage = Field(..., description="The usage of the completion")
    
    
class ChatCompletionRequest(BaseModel):
    model:str = Field(default="gpt-3.5-turbo-16k-0613", description="The model of the completion")
    messages:List[Message] = Field(..., description="The messages of the completion")
    
    
class OpenAIChat(ApiClient):
    def __init__(self, *args, **kwargs):
        super().__init__(base_url="https://api.openai.com/v1/", headers={
            "Authorization": f"Bearer {env.OPENAI_API_KEY}"
        }
        )
    
    async def chat(self, messages:List[Message]) -> ChatCompletionResponse:
        response = await self.fetch("chat/completions","POST",headers=self.headers, json=ChatCompletionRequest(messages=messages).dict())    
        assert isinstance(response, dict)
        return ChatCompletionResponse(**response)
    
    
```