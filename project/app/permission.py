from fastapi import Depends, FastAPI, HTTPException
from fastapi.routing import APIRoute
from starlette.status import HTTP_403_FORBIDDEN
from app.models.auth import RoleType, User

from app.user import UserInfo


class Permission:
    description: str = "<h2>🚀 필요한 권한 목록</h2>"
    permission_exception = HTTPException(
        status_code=HTTP_403_FORBIDDEN,
        detail={
            "errer": "Permission Denied",
            "error_description": 'Insufficient Permissions'
        },
        headers={"WWW-Authenticate": "Bearer"},
    )

    auth_exception = HTTPException(
        status_code=HTTP_403_FORBIDDEN,
        detail={
            "errer": "Permission Denied",
            "error_description": 'Permission Denied'
        },
        headers={"WWW-Authenticate": "Bearer"},
    )

    def __init__(self, input_permission: list):
        self.input_permission = input_permission

    def __call__(self, userinfo: User = Depends(UserInfo())):
        return self.check_user_permission_and_input_permission(userinfo, self.input_permission)

    @classmethod
    def check_user_permission_and_input_permission(cls, user_data: User, input_permission: list):
        user_permission = user_data.permission
        user_permission_list = cls.get_user_permission_list(user_permission)
        if cls.has_permission(user_permission_list, input_permission):
            return user_data
        raise cls.permission_exception

    @classmethod
    def get_user_permission_list(cls, user_permission: str):
        return [user_permission]

    @staticmethod
    def has_permission(user_permission: list, input_permission: list) -> bool:
        permission_length = len(list(set(input_permission) & set(user_permission)))
        return permission_length > 0

    @classmethod
    def route_description_edit_permission_text(cls, app: FastAPI) -> None:
        for route in app.routes:
            if isinstance(route, APIRoute):
                for depend in route.dependant.dependencies:
                    if isinstance(depend.call, Permission):
                        permission: Permission = depend.call
                        route.description += cls.get_description(permission.input_permission)

    @classmethod
    def get_description(cls, input_permission) -> str:
        description = cls.description
        role_list = RoleType.get_list()
        for perm in role_list:
            checked = ' checked' if perm in input_permission else ''
            description += "<input type='checkbox' name='{perm}' disabled{checked}/> <label for='{perm}'>{perm}</label> &nbsp;".format(perm=RoleType.get_text(perm), checked=checked)
        return description
