from aiofauna import *
from .typedefs import *
from geocoder import ip
from uuid import uuid4
from datetime import datetime


class User(Chainable):
    """
    Auth0 User, Github User or Cognito User
    """

    email: Optional[str] = Field(default=None, index=True)
    email_verified: Optional[bool] = Field(default=False)
    family_name: Optional[str] = Field(default=None)
    given_name: Optional[str] = Field(default=None)
    locale: Optional[str] = Field(default=None, index=True)
    name: str = Field(...)
    nickname: Optional[str] = Field(default=None)
    picture: Optional[str] = Field(default=None)
    sub: str = Field(..., unique=True)
    updated_at: Optional[str] = Field(default=None)
 
class Lead(Chainable):
    """
    A lead is a potential customer
    """

    email: str = Field(..., unique=True)
    name: str = Field(...)
    ip_address: Optional[str] = Field(default=None, index=True)
    geo: Optional[dict] = Field(default=None)

    @classmethod
    def from_request(cls, request: Request):
        """
        Creates a lead from a request
        """
        for field in cls.__fields__.values():
            if field.name == "ip_address":
                field.default = request.remote
            elif field.name == "geo":
                field.default = ip(request.remote).json["raw"]
        return cls


class Upload(FaunaModel):
    """

    S3 Upload Record

    """

    user: str = Field(..., description="User sub", index=True)
    name: str = Field(..., description="File name")
    key: str = Field(..., description="File key", unique=True)
    size: int = Field(..., description="File size", gt=0)
    type: str = Field(..., description="File type", index=True)
    lastModified: float = Field(
        default_factory=lambda: datetime.now().timestamp(),
        description="Last modified",
        index=True,
    )
    url: Optional[str] = Field(None, description="File url")


class DatabaseKey(FaunaModel):
    """

    Fauna Database Key

    """

    user:str = Field(..., unique=True)
    database: str = Field(...)
    global_id: str = Field(...)
    key: str = Field(...)
    secret: str = Field(...)
    hashed_secret: str = Field(...)
    role: str = Field(...)