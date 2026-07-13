from copy import deepcopy
from sqlalchemy.inspection import inspect


def clone_database_object(obj):
    cls = type(obj)
    mapper = inspect(cls)
    return cls(**{
        column.key: getattr(obj, column.key)
        for column in mapper.columns
        if not column.primary_key
    })


def clone_runtime_object(obj):
    return deepcopy(obj)
