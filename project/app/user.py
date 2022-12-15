from fastapi import Header
from fastapi.exceptions import HTTPException

from starlette.status import HTTP_401_UNAUTHORIZED

from app.models.auth import User

class UserInfo:
    async def __call__(self, token: str = Header()):
        try:
            userinfo = await self.get_user_by_token(token)
        except Exception as e:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail={
                    "errer": e.__class__.__name__,
                    "error_description": ' '.join(e.args)
                },
                headers={"WWW-Authenticate": "Bearer"},
            )
        return userinfo

    def get_user_by_token(self, token: str):
        return User.get_or_none(token=token)
