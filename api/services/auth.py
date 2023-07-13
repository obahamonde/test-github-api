import json
from os import environ
from aiofauna import *
from ..schemas import User


class AuthClient(ApiClient):
    async def user_info(self, token: str):
        try:
            user_dict = await self.fetch(
                f"{environ.get('AUTH0_DOMAIN')}/userinfo",
                headers={"Authorization": f"Bearer {token}"},
            )
            assert isinstance(user_dict, dict)
            return await User(**user_dict).save()

        except (AssertionError, HTTPException) as exc:
            return HTTPException(
                text=json.dumps({"status": "error", "message": str(exc)})
            )
