from __future__ import annotations

from aiofauna import *
from openai_function_call import openai_function, openai_schema

from ..schemas.typedefs import *
from .pinecone import *

Role = Literal["user", "assistant", "system", "function"]


class Message(BaseModel):
    role: Role = Field(..., description="The role of the message")
    content: str = Field(..., description="The content of the message")


class Choice(BaseModel):
    message: Message = Field(..., description="The message of the choice")
    index: int = Field(..., description="The index of the choice")
    finish_reason: Optional[str] = Field(
        None, description="The finish reason of the choice"
    )


class ChatCompletionResponse(BaseModel):
    id: str = Field(..., description="The id of the completion")
    object: str = Field(..., description="The object of the completion")
    created: int = Field(..., description="The created timestamp of the completion")
    choices: List[Choice] = Field(..., description="The choices of the completion")
    usage: Usage = Field(..., description="The usage of the completion")


class ChatCompletionRequest(BaseModel):
    model: str = Field(
        default="gpt-3.5-turbo-16k-0613", description="The model of the completion"
    )
    messages: List[Message] = Field(..., description="The messages of the completion")


class OpenAIChat(ApiClient):
    def __init__(self, *args, **kwargs):
        super().__init__(
            base_url="https://api.openai.com/v1/",
            headers={"Authorization": f"Bearer {env.OPENAI_API_KEY}"},
        )

    async def chat(self, messages: List[Message]) -> ChatCompletionResponse:
        response = await self.fetch(
            "chat/completions",
            "POST",
            headers=self.headers,
            json=ChatCompletionRequest(messages=messages).dict(),
        )
        assert isinstance(response, dict)
        return ChatCompletionResponse(**response)
