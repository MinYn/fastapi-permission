from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

from enum import Enum

class RoleType(str, Enum):
    OWNER = 'owner'
    EDITOR = 'editor'
    VIEWER = 'viewer'

    __text__ = dict({
        OWNER: '소유자',
        EDITOR: '편집자',
        VIEWER: '뷰어',
    })

    @classmethod
    def get_text(cls, member):
        return cls.__text__[member]

    @classmethod
    def get_list(cls):
        return list(map(lambda c: c.value, RoleType))


class User(models.Model):
    token = fields.TextField()
    permission = fields.CharEnumField(RoleType)


PermissionSchema = pydantic_model_creator(User)
