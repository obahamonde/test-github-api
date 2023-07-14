from importlib import metadata
from numpy import isin
from ..schemas.typedefs import *
from aiofauna import *
from uuid import uuid4
from pydantic import Field
from ..config import env

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
    top_k:int = Field(default=8)
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
        print(response)
    
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