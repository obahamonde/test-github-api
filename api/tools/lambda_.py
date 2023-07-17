from ..schemas import *
from ..services import *
from ..config import env


class Lambdafunction(Chainable):
    name: str = Field(
        ..., description="Name of the function deployment", alias="FunctionName"
    )
    role: str = Field(
        env.AWS_LAMBDA_ROLE, description="Role of the function deployment", alias="Role"
    )
    runtime: str = Field(
        "python3.10", description="Runtime of the function deployment", alias="Runtime"
    )
    handler: str = Field(
        "main.handler",
        description="Handler of the function deployment",
        alias="Handler",
    )
    timeout: int = Field(
        30, description="Timeout of the function deployment", alias="Timeout"
    )
    memory_size: int = Field(
        128, description="Memory size of the function deployment", alias="MemorySize"
    )
    publish: bool = Field(
        True, description="Publish of the function deployment", alias="Publish"
    )
    code: Dict[str, str] = Field(
        ..., description="Code of the function deployment", alias="Code"
    )
    environment: Dict[str, str] = Field(
        ..., description="Environment of the function deployment", alias="Environment"
    )
    url: str = Field(..., description="Url of the function deployment", alias="Url")

    @property
    def session(self) -> Session:
        return Session(
            aws_access_key_id=env.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=env.AWS_SECRET_ACCESS_KEY,
            region_name=env.AWS_REGION,
        )

    async def lambda_endpoint(self) -> Dict[str, Any]:
        async with self.session.client("lambda") as lambda_:
            response = await lambda_.create_function(**self.dict())
            url = await lambda_.create_function_url_config(
                FunctionName=response["FunctionName"],
                AuthType="NONE",
                Cors={
                    "AllowOrigins": ["*"],
                    "AllowMethods": ["*"],
                    "AllowHeaders": ["*"],
                    "AllowCredentials": True,
                    "ExposeHeaders": ["*"],
                    "MaxAge": 86400,
                },
            )
            await lambda_.add_permission(
                FunctionName=response["FunctionName"],
                StatementId=uuid4().hex,
                Action="lambda:InvokeFunctionUrl",
                Principal="*",
                FunctionUrlAuthType="NONE",
            )
            self.url = url["Url"]
            return {
                "instance": self,
                "response": response,
            }

    async def lambda_delete(self) -> Dict[str, Any]:
        async with self.session.client("lambda") as lambda_:
            response = await lambda_.delete_function(FunctionName=self.name)
            return {
                "instance": self,
                "response": response,
            }
